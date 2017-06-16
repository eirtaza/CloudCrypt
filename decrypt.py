import binascii
from Crypto.Cipher import AES
import os

padding = 0;

def unpad(s):
	diff = len(s) % 16
	global padding
	padding = int (s[-diff:])
	#print "Padding:" + str(padding)
	s = s[:-diff]
	#print "Return Length:" + str(len(s)) 
	return s

def decrypt(k, iput, oput):

	key = k
	key = binascii.unhexlify(key)

	f = open(iput, 'rb')
	contents = f.read()
	contents = unpad(contents)
	iv = contents[-16:]
	print "\tIV:" + iv

	contents = contents[:-16]

	encobj = AES.new(key, AES.MODE_CBC, iv)
	plain = encobj.decrypt(contents)
	if padding != 0:
		plain = plain[:-padding]

	f = open(oput[:-3], "wb")
	f.write(plain)
	f.close()