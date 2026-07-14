#!/usr/bin/env python3
import os
import re
import sqlite3
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
    files = sorted([f for f in os.listdir(PORTRAIT_DIR) if os.path.isfile(os.path.join(PORTRAIT_DIR, f))])
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # assign Elosha explicitly
    cur.execute("SELECT Id FROM Characters WHERE Name = ?", ('Elosha',))
    row = cur.fetchone()
    if row:
        cid = row[0]
        cur.execute('UPDATE Characters SET Portrait = ? WHERE Id = ?', ('images/portraits/Elosha Portrait.png', cid))
        conn.commit()
        print('Assigned Elosha Id', cid)
    else:
        print('Elosha not found')

    cur.execute('SELECT Id, Name, Portrait FROM Characters')
    chars = cur.fetchall()
    assigned_files = set()
    for cid, name, portrait in chars:
        if portrait:
            assigned_files.add(os.path.basename(portrait))

    full_map = {}
    nick_map = {}
    for cid, name, portrait in chars:
        nf = norm(name)
        full_map[nf] = (cid, name)
        m = re.search(r'"([^"]+)"', name)
        if m:
            nn = norm(m.group(1))
            nick_map[nn] = (cid, name)

    def best_match(n):
        best = None
        best_score = 0.0
        best_kind = 'full'
        for k, v in nick_map.items():
            s = SequenceMatcher(None, n, k).ratio()
            if s > best_score:
                best_score = s
                best = v
                best_kind = 'nick'
        for k, v in full_map.items():
            s = SequenceMatcher(None, n, k).ratio()
            if s > best_score:
                best_score = s
                best = v
                best_kind = 'full'
        return best, best_score, best_kind

    auto_assigned = []
    unmatched = []
    for f in files:
        if f in assigned_files:
            continue
        base = os.path.splitext(f)[0]
        n = norm(base)
        best, score, kind = best_match(n)
        if best and score >= 0.7:
            cid, name = best
            portrait_val = os.path.join('images/portraits', f)
            cur.execute('UPDATE Characters SET Portrait = ? WHERE Id = ?', (portrait_val, cid))
            auto_assigned.append((f, cid, name, round(score, 3), kind))
        else:
            unmatched.append((f, round(score, 3)))

    conn.commit()

    print('\nAuto-assigned:')
    for a in auto_assigned:
        print(a)

    print('\nUnmatched:')
    for u in unmatched:
        print(u)

    print('\nSummary: auto-assigned', len(auto_assigned), 'files;', len(unmatched), 'unmatched remaining.')
    conn.close()


if __name__ == '__main__':
    main()
