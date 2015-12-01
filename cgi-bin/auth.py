#!/usr/bin/env python

import cgi, json, match
from user import user

import time
import sys
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Hash import SHA

def decrypt(cipherText, password):
    time_s = time.time()
    cipherText = cipherText.decode('hex')
    # Generate key from password
    key = MD5.new(password).hexdigest().decode('hex')
    # Decrypt the ciphertext
    iv = cipherText[:16]

    # iv = ('ee445d5f8169204c77d445aa4688eae7').decode('hex')
    dec = cipherText[16:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(dec)
    # print "%s" % decrypted
    
    # Extract the hash, pattern and time
    para = decrypted.split('###')
    if len(para) < 4:
        return False
    hash_recv, pattern_recv, time_recv = para[0], para[1], para[2]

    # compare hash
    hash_s = SHA.new(pattern_recv + time_recv).hexdigest()
    if hash_s != hash_recv:
        # print "hash doesn't match!"
        return False

    # compare time
    time_recv = float(time_recv) / 1000
    if time_s - time_recv > 20 or time_s < time_recv:
        # print "Invalid time!"
        return False
    return pattern_recv
    # If match
        # Convert the pattern into Python array
        # return the array
    # else
        # return false

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
