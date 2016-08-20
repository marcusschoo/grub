import plistlib
import argparse

from grub.recipe import Recipe
from grub.product import Product
from grub.product import Ingredient
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
        if mg_recipe['SOURCE']:
            if mg_recipe['PUBLICATION_PAGE']:
                grub_recipe.location = mg_recipe['SOURCE'] + " (%s)" % mg_recipe['PUBLICATION_PAGE']
            else:
                grub_recipe.location = mg_recipe['SOURCE']
        for mg_ingredient in mg_recipe['INGREDIENTS']:
            grub_product = grub_db.find_product_by_name(mg_ingredient['DESCRIPTION'])
            if not grub_product:
                grub_product = Product(mg_ingredient['DESCRIPTION'])
                grub_db.save_product(grub_product)
            new_ingredient = Ingredient(grub_product, mg_ingredient['QUANTITY'], mg_ingredient['MEASUREMENT'])
            grub_recipe.ingredients.append(new_ingredient)
        grub_db.save_recipe(grub_recipe)

print 'Done'

#python macgourmet_to_grub.py macgourmet_export.plist grub.plist