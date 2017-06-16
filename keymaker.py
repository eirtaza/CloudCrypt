from ConfigParser import SafeConfigParser
import os, sys
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

__doc__ = """Key manager module"""

def make(pwd):
    password = pwd

    for i in range(565432):
        hash = SHA256.new()
        hash.update(password)
        password = hash.digest()
    print "Password hash: " + password.encode('hex')

    #pbkdf2 stuff
    #init pbkdf2 values
    iterations = 50000
    key = ''
    # Static salt is defined
    # This won't cause any security breach
    salt = '#49^#vEos@i!2S-4'
    # Generate key using PBKDF2
    key = PBKDF2(password, salt, dkLen=32, count=iterations)
    key = key.encode('hex')

    if os.path.isfile('hash'):
        print "Hash file exists ... OK"
        hashfile = open('hash', 'r')
        hashFileValue = hashfile.read()
        if hashFileValue == password:
            print "Correct Password"
            return key
        else:
            print "Mismatched Password"
            return None
        
    else:
        print "Hash file does not exist"
        print "Creating new Hash file . . . "

        parser = SafeConfigParser()
        parser.read('config.ini')
        dest = parser.get('paths', 'dest')

        if os.path.exists(dest + "/hash") is False:
            remote_file = open(dest + "/hash","w")
            remote_file.write(password)
            remote_file.close()

        f = open(dest + "/hash", 'r')
        remote = f.read()

        if remote == password:
            output_file = open("hash","w")
            output_file.write(password)
            output_file.close()
        else:
            print "\n\nRemote hash mismatch.\nDid you use this account with another password?\nTry using your actual password."
            sys.exit()

        return key