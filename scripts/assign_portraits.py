#!/usr/bin/env python3
import os
import sqlite3
import re
from difflib import SequenceMatcher, get_close_matches

DB = 'app.db'
PORTRAIT_DIR = 'wwwroot/images/portraits'

FILES = sorted([f for f in os.listdir(PORTRAIT_DIR) if os.path.isfile(os.path.join(PORTRAIT_DIR, f))])

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('SELECT Id, Name, Portrait FROM Characters')
chars = cur.fetchall()

# Normalization helper
def norm(s: str) -> str:
    if s is None:
        return ''
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '', s)
    return s

char_map = {norm(name): (cid, name) for cid, name, portrait in chars}
char_norms = list(char_map.keys())
char_names_by_norm = {k: v[1] for k, v in char_map.items()}

auto_assigned = []
ambiguous = []
unmatched = []

for f in FILES:
    base = os.path.splitext(f)[0]
    n = norm(base)
    if n in char_map:
        cid, name = char_map[n]
        portrait_val = os.path.join('images/portraits', f)
        cur.execute('UPDATE Characters SET Portrait = ? WHERE Id = ?', (portrait_val, cid))
        auto_assigned.append((f, cid, name))
        continue

    # compute best matches
    best = None
    best_score = 0.0
    for cn in char_norms:
        s = SequenceMatcher(None, n, cn).ratio()
        if s > best_score:
            best_score = s
            best = cn

    if best_score >= 0.92:
        cid, name = char_map[best]
        portrait_val = os.path.join('images/portraits', f)
        cur.execute('UPDATE Characters SET Portrait = ? WHERE Id = ?', (portrait_val, cid))
        auto_assigned.append((f, cid, name, round(best_score, 3)))
    elif best_score >= 0.7:
        # show top 3 close matches
        candidates = get_close_matches(n, char_norms, n=3, cutoff=0.0)
        cand_list = [(c, char_names_by_norm[c], round(SequenceMatcher(None, n, c).ratio(),3)) for c in candidates]
        ambiguous.append((f, base, best_score, cand_list))
    else:
        unmatched.append((f, base, best_score))

conn.commit()

print('Auto-assigned (updated Characters.Portrait):')
for a in auto_assigned:
    print(a)

print('\nAmbiguous (please review and confirm mapping):')
for a in ambiguous:
    print(a)

print('\nUnmatched:')
for u in unmatched:
    print(u)

conn.close()
