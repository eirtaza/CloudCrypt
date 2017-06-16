import binascii
from Crypto.Cipher import AES
import os

def pad(s):
	if (len(s) % 16) == 0:
		return s
	else:
		diff = 16 - len(s) % 16
		p = os.urandom(diff)
		s = s + p
		return s

def encrypt(k, iput, oput):
	iv = os.urandom(8)
	iv = iv.encode('hex')

	key = k
	key = binascii.unhexlify(key)

	f = open(iput, 'rb')
	contents = f.read()

	padded = pad(contents)

	encobj = AES.new(key, AES.MODE_CBC, iv)
	crypted = encobj.encrypt(padded)
	crypted = crypted + iv
	crypted = crypted + str(len(padded) - len(contents))

	f = open(oput + ".enc", "wb")
	f.write(crypted)
	f.close()


