import plistlib
import argparse

from grub.recipe import Recipe
from grub.database import Database

argparser = argparse.ArgumentParser(description="Command line to convert macgourmet export plist to Grub.")
argparser.add_argument('macgourmet_file',
                       help='The macgourmet recipe export to convert')
argparser.add_argument('grub_file',
                       help='The file to write the grub data to')
args = argparser.parse_args()

if args.macgourmet_file and args.grub_file:
    print 'Convert', args.macgourmet_file, 'to', args.grub_file
    grub_db = Database(file_path=args.grub_file)
    macgourmet_data = plistlib.readPlist(args.macgourmet_file)
    for mg_recipe in macgourmet_data:
        grub_recipe = Recipe(name=mg_recipe['NAME'], directions=mg_recipe['DIRECTIONS'])
        grub_db.save_recipe(grub_recipe)

print 'Done'