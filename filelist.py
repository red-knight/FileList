import hashlib
import optparse
import os

## Get md5sum of listed file and return
def md5sum(fname):
	hash_md5 = hashlib.md5()
	# Read file a bit at a time so we don't run out of RAM
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def openup(list):
	file = open(list,"r")
	return file


## Main
def main():
	#do some stuff
	parser = optparse.OptionParser()

	parser.add_option('-f', '--file',
    	action="store", dest="file",
    	help="File to process", default="")

	parser.add_option('-d', '--directory',
    	action="store", dest="dir",
    	help="Directory to process", default="")

	options, args = parser.parse_args()

	if not options.file and not options.dir:
		options.dir = os.getcwd()

	print("file is " + options.file + " and dir is " + options.dir)

	#file = openup(options.file)
	result = md5sum(options.file)

	print("md5 is " + result)

if __name__ == '__main__':
	main()