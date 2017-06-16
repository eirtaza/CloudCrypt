from ConfigParser import SafeConfigParser
import sys
import os
import keymaker
import encrypt, decrypt

# parse configuration
parser = SafeConfigParser()
parser.read('config.ini')
dest = parser.get('paths', 'dest')
print "Encrypted folder path: " + dest

# Check for target folder & data folder
if os.path.isdir(dest) is False:
	print "Target folder does not exist"
	print "Exiting CloudCrypt"
	sys.exit()
if os.path.isdir("./data") is False:
	os.makedirs("data")
	print "Please save files to be encrypted in 'data' folder under CloudCrypt"

print "Target & Source folders found"

password = raw_input("\nEnter Password: ")

key = keymaker.make(password)

if key is None:
	print "\nExiting CloudCrypt"
	sys.exit()

# Sync
print "\nSync ..."

rootDir = 'data'
for dirName, subdirList, fileList in os.walk(rootDir):
	print ('\nEncrypting Dir: %s' % dirName)
	if os.path.isdir(dest + "\\" + dirName):
		print "Foler Exists!"
	else:
		os.makedirs(dest + "\\" + dirName)
		print "Folder Created!"


	for fname in fileList:
		print "\t" + dirName + "\\" + fname
		if os.path.exists(dest + "/"+ dirName +"/" + fname + ".enc"):
			print "\tAlready sync "
		else:
			encrypt.encrypt(key, dirName +"\\"+ fname, dest + "\\" + dirName + "\\" + fname)


# Rev Sync
print "\n\nStarting Reverse Sync\n\n"

rootDir = dest + "\\" + 'data'
chop = len(dest) + 1
for dirName, subdirList, fileList in os.walk(rootDir):
	print ('\nDecrypting to Local Dir: %s' % dirName)
	if os.path.isdir("./" + dirName[chop:]):
		print "Local Foler Exists!"
	else:
		os.makedirs("./" + dirName[chop:])
		print "Local Folder Created"

	for fname in fileList:
		print "\t" + dirName + "\\" + fname
		if fname[-4:] == ".enc":
			if os.path.exists("./" + dirName[chop:] + "//" + fname[:-3]):
				print "\tAlready sync "
			else:
				decrypt.decrypt(key, dirName + "/" + fname, "./" + dirName[chop:] + "/" + fname)
		else:
			print "File skipped"



print '\n Sync Complete!'