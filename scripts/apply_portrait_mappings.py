#!/usr/bin/env python3
import os
import sqlite3

DB = 'app.db'
ASSIGNMENTS = {
    'Felix.png': 'Felix Gaeta',
    'Gaius Alt.png': 'Gaius Baltar (Alternative)',
    'Helo Original.png': 'Karl "Helo" Agathon (Original)',
    'Hera Portrait.png': 'Hera Agathon',
    'Kendra Portrait.png': 'Kendra Shaw',
    'Laura.png': 'Laura Roslin',
    'Louis.png': 'Louis Hoshi',
    'Romo.png': 'Romo Lampkin',
    'Sam.png': 'Samuel T. Anders',
    'Saul.png': 'Saul Tigh',
    'Simon.png': "Simon O'Neill",
    'Tory.png': 'Tory Foster',
    'Zerek Alt.png': 'Tom Zarek (Alternative)',
    'Zerek.png': 'Tom Zarek (Original)',
}


def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    for file_name, char_name in ASSIGNMENTS.items():
        cur.execute('SELECT Id FROM Characters WHERE Name = ?', (char_name,))
        row = cur.fetchone()
        if row is None:
            print('MISSING CHARACTER:', char_name)
            continue
        cid = row[0]
        portrait_path = f'images/portraits/{file_name}'
        cur.execute('UPDATE Characters SET Portrait = ? WHERE Id = ?', (portrait_path, cid))
        print('Updated', file_name, '->', char_name, 'Id', cid)

    conn.commit()

    cur.execute('SELECT Portrait FROM Characters WHERE Portrait IS NOT NULL')
    assigned = {os.path.basename(r[0]) for r in cur.fetchall()}
    files = sorted([f for f in os.listdir('wwwroot/images/portraits') if os.path.isfile(os.path.join('wwwroot/images/portraits', f))])
    remaining = [f for f in files if f not in assigned]

    print('\nRemaining unassigned:', len(remaining))
    for f in remaining:
        print(f)

    conn.close()


if __name__ == '__main__':
    main()
