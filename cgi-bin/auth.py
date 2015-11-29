#!/usr/bin/env python

import cgi, json, match
from user import user

def decrypt(ciphertext, password):
    # Generate key from password

    # Decrypt the ciphertext
    
    # Extract the pattern and compute the hash

    # Extract the hash and compare

    # If match
        # Convert the pattern into Python array
        # return the array
    # else
        # return false
    return ciphertext

data = cgi.FieldStorage()
msg = json.loads(data['msg'].value)
u = user.get(msg['username'])

is_match = False
similarity = 0

if u:
    plaintext = decrypt(msg['ciphertext'], u.password)

    if plaintext:
        pattern = json.loads(plaintext)
        is_match, similarity = match.match(pattern, u.pattern)
    
        if is_match:
            u.add_pattern(pattern)
            error = ''
        else:
            error = 'Timing pattern doesn\'t match.'
    else:
        error = 'Wrong password.'
else:
    error = 'No such user.'
    
print 'Content-Type: application/json'
print
print json.dumps([is_match, similarity, error])
