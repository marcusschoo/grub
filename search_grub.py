import plistlib
import argparse

from grub_api.recipe import Recipe
from grub_api.database import Database

# mace??
# quinoa cooked
# first and second mixture
# spinach chopped
# stove
# tent pegs
# unbaked pie crust

argparser = argparse.ArgumentParser(description="Command line to convert macgourmet export plist to Grub.")
argparser.add_argument('macgourmet_file',
                       help='The macgourmet recipe export to convert')
argparser.add_argument('product_name',
                       help='Product name to search for')
args = argparser.parse_args()

if args.macgourmet_file:
    print 'Searching recipes in', args.macgourmet_file, 'for product', args.product_name
    macgourmet_data = plistlib.readPlist(args.macgourmet_file)
    for mg_recipe in macgourmet_data:
        for mg_ingredient in mg_recipe['INGREDIENTS']:
            if args.product_name in mg_ingredient['DESCRIPTION']:
                print 'matches', mg_ingredient['DESCRIPTION'], 'in', mg_recipe['NAME']

print 'Done'