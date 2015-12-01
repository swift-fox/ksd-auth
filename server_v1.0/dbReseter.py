import sqlite3 as db
import sys
import os









if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python dbReseter.py <database folder>"
        sys.exit(1)

    root = sys.argv[1] if sys.argv[1][-1] == '/' else sys.argv[1]+'/'

    if not os.path.isdir(root):
        os.makedirs(root)

    conn = db.connect(root+'project.db')
    cur = conn.cursor()
   
    try:
        cur.execute('DROP TABLE users')
    except db.Error:
        pass
    try:
        cur.execute('DROP TABLE patterns')
    except db.Error:
        pass

    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, credential TEXT NOT NULL, trainedPattern TEXT)")
    cur.execute("CREATE TABLE patterns(id INTEGER PRIMARY KEY, username TEXT NOT NULL, pattern TEXT NOT NULL)")

    conn.commit()

    conn.close()

    print "database resetted"



