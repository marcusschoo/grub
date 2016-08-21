import plistlib
import argparse
import subprocess
import tempfile
import os

from grub_api.recipe import Recipe
from grub_api.database import Database

argparser = argparse.ArgumentParser(description="Command line to edit Grub recipe category contents.")
argparser.add_argument('grub_file',
                       help='The file to write the grub data to')
args = argparser.parse_args()

if args.grub_file:
    print 'Edit recipe categories of', args.grub_file
    category_file = tempfile.NamedTemporaryFile(mode='w+b',delete=False)
    # Should print list of all recipes and current categories
    category_file.write('hello\n')
    category_file.close()
    print category_file.name
    subprocess.call(["open","-e","-W",category_file.name])
    # should read file and update categories in db
    with open(category_file.name,'r') as the_file:
	    for l in the_file:
	    	print '...', l
	# remove the temporary file
    os.remove(category_file.name)
print 'Done'