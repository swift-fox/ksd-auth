#!/usr/bin/env python

import cgi, json, match
from user import user

data = cgi.FieldStorage()
msg = json.loads(data['msg'].value)
u = user.get(msg['username'])
password = msg['password']

is_match = False
similarity = 0

if u:
    if u.password == password:
        pattern = msg['pattern']
        is_match, similarity = match.match(pattern, u.pattern)

        if is_match:
            u.add_pattern(pattern)
            error = 'Authentication successful.'
        else:
            error = 'Timing pattern doesn\'t match.'
    else:
        error = 'Wrong password.'
else:
    error = 'No such user.'
    
print 'Content-Type: application/json'
print
print json.dumps([is_match, similarity, error])
