#!/usr/bin/env python3
import os
import sqlite3
import re
from difflib import SequenceMatcher

DB = 'app.db'
PORTRAIT_DIR = 'wwwroot/images/portraits'


def norm(s):
    if not s:
        return ''
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '', s)
    return s


def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT Id, Name, Portrait FROM Characters')
    chars = cur.fetchall()
    char_entries = []
    for cid, name, portrait in chars:
        full = norm(name)
        nick = None
        m = re.search(r'"([^"]+)"', name)
        if m:
            nick = norm(m.group(1))
        char_entries.append((cid, name, full, nick))

    files = sorted([f for f in os.listdir(PORTRAIT_DIR) if os.path.isfile(os.path.join(PORTRAIT_DIR, f))])
    cur.execute('SELECT Portrait FROM Characters WHERE Portrait IS NOT NULL')
    assigned = set(os.path.basename(r[0]) for r in cur.fetchall())

    for f in files:
        if f in assigned:
            continue
        base = os.path.splitext(f)[0]
        n = norm(base)
        candidates = []
        for cid, name, full, nick in char_entries:
            if nick:
                s = SequenceMatcher(None, n, nick).ratio()
                candidates.append((s, 'nick', cid, name))
            s2 = SequenceMatcher(None, n, full).ratio()
            candidates.append((s2, 'full', cid, name))
        best_by_cid = {}
        for score, kind, cid, name in candidates:
            if cid not in best_by_cid or score > best_by_cid[cid][0]:
                best_by_cid[cid] = (score, kind, name)
        top = sorted([(v[0], v[1], k, v[2]) for k, v in best_by_cid.items()], key=lambda x: x[0], reverse=True)[:3]
        print(f"{f} ->")
        for score, kind, cid, name in top:
            print(f"  {score:.3f}\t{kind}\t{cid}\t{name}")
        print()
    conn.close()


if __name__ == '__main__':
    main()
