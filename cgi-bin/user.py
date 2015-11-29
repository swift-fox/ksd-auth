#!/usr/bin/env python

import sqlite3, os, json, config, match

class user:
    conn = sqlite3.connect(config.db)

    def __init__(self, uid, username, password, pattern):
        self.uid = uid
        self.username = username
        self.password = password
        self.pattern = pattern

    def add_pattern(self, pattern):
        c = user.conn.cursor()
        c.execute("INSERT INTO pattern_record VALUES(?, ?)", (self.uid, json.dumps(pattern)))

        # Do training when collected enough patterns
        c.execute("SELECT count(*) FROM pattern_record WHERE uid = ?", (self.uid,))
        count = c.fetchone()[0]
        if count >= config.training_size:
            c.execute("SELECT pattern FROM pattern_record WHERE uid = ?", (self.uid,))
            dataset = [json.loads(pattern[0]) for pattern in c.fetchall()]

            pattern = match.train(dataset)
            c.execute("UPDATE users SET pattern = ? WHERE rowid = ?", (json.dumps(pattern), self.uid))
            c.execute("DELETE FROM pattern_record WHERE uid = ?", (self.uid,))

        user.conn.commit()

    # Retrieve user info from the database. Return None if not exist.
    @staticmethod
    def get(username):
        row = user.conn.execute('SELECT rowid, * FROM users WHERE username = ?', (username,)).fetchone()
        return user(row[0], row[1], row[2], json.loads(row[3])) if row else None

    # Create a user. Return None is already exists
    @staticmethod
    def new(username, password, pattern):
        try:
            c = user.conn.execute('INSERT INTO users VALUES(?, ?, ?)', (username, password, json.dumps(pattern)))
        except sqlite3.IntegrityError:  # Violates the UNIQUE constrain on the username column
            return None

        user.conn.commit()
        return user(c.lastrowid, username, password, pattern)

    # Initialize the database.
    @staticmethod
    def init():
        user.conn.close()
        os.remove(config.db)
        user.conn = sqlite3.connect(config.db)

        user.conn.execute('CREATE TABLE users(username TEXT UNIQUE, password TEXT, pattern TEXT)');
        user.conn.execute('CREATE TABLE pattern_record(uid INTEGER, pattern TEXT)');
        user.conn.commit()

if __name__ == '__main__':
    import cgi

    data = cgi.FieldStorage(keep_blank_values = True)
    if 'new' in data:
        # Create a user
        msg = json.loads(data['msg'].value)
        u = user.new(msg['username'], msg['password'], msg['pattern'])

        print 'Content-Type: application/json'
        print
        print json.dumps(u != None)
    else:
        # Initialize the database
        print 'Content-Type: text/html'
        print
    
        print '''<html>
<head>
<title>Database Initialization</title>
</head>
<body>'''
        if 'init' in data:
            user.init()
            print '<p>Database initialized.</p>'
            print '<p><a href="javascript:history.go(-1)">Go Back</a></p>'
        else:
            print '<p><a href="?init">Initialize database</a></p>'
            print '<p><b>Warning:</b> all data will be wiped.</p>'
            
            print '<table>'
            print '<tr><th>UID</th><th>Username</th><th>Password</th><th>Pattern</th></tr>'
            users = user.conn.execute('SELECT rowid, * FROM users')
            for u in users:
                print '<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (u[0], u[1], u[2], u[3])
            print '</table>'

        print '</body>'
        print '</html>'
