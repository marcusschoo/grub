import plistlib
import argparse
from fractions import Fraction

from grub_api.recipe import Recipe
from grub_api.product import Product
from grub_api.product import Ingredient
from grub_api.database import Database


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
                try:
                    grub_product = Product(mg_ingredient['DESCRIPTION'])
                    grub_db.add_product(grub_product)
                except:
                    pass
            if grub_product:
                quantity = mg_ingredient['QUANTITY']
                if not quantity or quantity == '(null)':
                    quantity = None
                else:
                    quantity = float(Fraction(quantity))
                new_ingredient = Ingredient(grub_product,
                    quantity,
                    mg_ingredient['MEASUREMENT'] if mg_ingredient['MEASUREMENT'] else None)
                grub_recipe.ingredients.append(new_ingredient)
        grub_db.add_recipe(grub_recipe)

    grub_db.save(args.grub_file)

print 'Done'

#python macgourmet_to_grub.py macgourmet_export.plist grub.plist