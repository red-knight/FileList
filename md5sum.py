
import json
from optparse import OptionParser
import hashlib
import os

def getArgv():
	parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
	parser.add_option("-f", "--file", dest="filename", action="store",
					help="File to process")
	parser.add_option("-d", "--dir", dest="rootdir", action="store",
					help="Directory to process.")
	parser.add_option("-r", "--recursive", dest="recursive", action="store_true",
					help="Recursive flag.")
	parser.add_option("-j", "--json", dest="jsonFile", action="store",
					help="Result file to process.")

	(options, args) = parser.parse_args()
	#TODO Check for trailing slash on rootdir
	return(options.filename, options.rootdir, options.recursive, options.jsonFile)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def loopDir(dname, recursive):
	print("Looping through " + dname)
	filelist={}
	for filename in os.listdir(dname):
		print("Checking for object status: " + filename)
		#TODO handle permission issues
		if os.path.isdir(str(dname+'/'+filename)) and recursive:
			#print("Skipping directory: " + filename)
			filelist.update(loopDir(str(dname+'/'+filename), recursive))
		elif os.path.isfile(str(dname+'/'+filename)):
			print("Processing: " + dname + '/' + filename)
			filelist[str(dname+'/'+filename)]={}
			hashback = md5(str(dname+'/'+filename))
			filelist[str(dname+'/'+filename)]['name'] = str(dname+'/'+filename)
			filelist[str(dname+'/'+filename)]['hash'] = hashback
	return filelist

def writeJson(json):
	with open("results.json", "a") as f:
		f.write(json)
		f.close()

def readJson(jsonFile):
	jsonList = {}
	with open(jsonFile, "r") as f:
		jsonList = json.loads(f.read())
	return jsonList

def verifySums(json):
	# Check md5sums of listed files and ensure they're the same
	for filename in json:
		test = md5(str(json[filename]['name']))
		if test == str(json[filename]['hash']):
			print("no problemo")
		else:
			print("ruh roh")

def main():
	(filename, rootdir, recursive, jsonFile) = getArgv()

	if filename:
		# Just checking a single file
		print("Specified a single file:" + filename)
		hashback=md5(filename)
		print("Processed file, and hash is: " + hashback)
	elif rootdir:
		# Checking a whole dir of files
		print("Specified a directory:" + rootdir)
		filelist = loopDir(rootdir, recursive)
		for filename in filelist:
			print("Processed " + filelist[filename]['name'] + ", and hash is: " + filelist[filename]['hash'])
		if recursive:
			print("Recursive flag set.")

		# Convert filelist to json
		jsonList = json.dumps(filelist, indent=4, sort_keys=True)
		print(jsonList)

		# Write to file
		writeJson(jsonList)
	elif jsonFile:
		# Process results from a previous run.
		jsonList = readJson(jsonFile)
		results = verifySums(jsonList)

if __name__ == '__main__':
	main()