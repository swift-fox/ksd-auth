import time
import sys
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Hash import SHA

# print time.time()
# encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")

# BS = 16
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
# unpad = lambda s : s[0:-ord(s[-1])]

# password = "123456"
# pattern = 'sjw'
# time = 0


# key = MD5.new(password).hexdigest()
# print key
# # iv = Random.new().read(AES.block_size)
# iv = '0' * 32
# key = key.decode('hex')
# iv = iv.decode('hex')


# hash = SHA.new(pattern + str(time)).hexdigest()
# message = hash + '#' + pattern + '#' + str(time) + '#'
# print message, len(message)

# # message must be a multiple of 16 in length
# # message = pad(message)
# print message, len(message)
# aes = AES.new(key, AES.MODE_CBC, iv)
# cypherText = aes.encrypt(message)
# cypherText = cypherText.encode('hex')
# print cypherText

# aes = AES.new(key, AES.MODE_CBC, iv)
# cypherText = '6c7bdf18c2256ebb82f74a4abeafabc35d8692bd1abe1a97fe9471ee121cfd7d22714873d2ccdef3951f26a676ddca0a2e4d6e082397337bafbfc7b198fbdc75'
# cypherText = cypherText.decode('hex')
# decrypted = aes.decrypt(cypherText)
# print "%s" % decrypted


# key = MD5.new(password).hexdigest()
# # key = ('2411d8ab7f08e41d814c0909d7f02aa19d3527ccd2e5a691faa0ea10c0faeaa0').decode('hex')
# print key
# salt = ('d1165d210db84575').decode('hex');
# iv = ('c3e0f3bd9a592518c98d5a12750f4ef0').decode('hex')
# aes = AES.new(salt, key, AES.MODE_CBC, iv)
# cypherText = 'cddfc66d91c9864662b646b8e8d64a28f94531cd38eb81baa5e3bbec3c8f1f5d528d410f284336268be65e7276ba2c8f'
# cypherText = cypherText.decode('hex')
# decrypted = aes.decrypt(cypherText)
# print "%s" % decrypted


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
    print "%s" % decrypted
    
    # Extract the hash, pattern and time
    para = decrypted.split('###')
    hash_recv, pattern_recv, time_recv = para[0], para[1], para[2]

    # compare hash
    hash_s = SHA.new(pattern_recv + time_recv).hexdigest()
    print hash_s
    if hash_s != hash_recv:
    	print "hash doesn't match!"
    	return False

    # compare time
    time_recv = float(time_recv) / 1000
    print time_s
    print time_recv
    if time_s - time_recv > 20 or time_s < time_recv:
    	print "Invalid time! "
    	return False
    print pattern_recv
    return pattern_recv
    # If match
        # Convert the pattern into Python array
        # return the array
    # else
        # return false
    

cipherText = '000000000000000000000000000000003a4b25a1d08062daf1e59ea5c557620ff49c85757ad55a3d055fb68b631a11f0e118386e7773dffb7e5c010fe5dbfaa89422ec93b0db4bcb7b9aca499205a1d4e38b24ca9a565ab6b4fbb30965185b9ea4d713f163af2cb1c9ce6fab8d2f2731'
password = '123456abcdef'
decrypt(cipherText, password)

