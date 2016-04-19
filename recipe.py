import argparse
import plistlib
import uuid

FILE_PATH = './recipes.plist'

def save():
    plistlib.writePlist(db, FILE_PATH)

def printNames(db):
    for r in db:
        print r['NAME']

def parseMenu( file ):
    menu = []
    index = 0
    for l in file.readlines():
        if l.startswith('y '):
            menu.append(index)
        index = index + 1
    return menu

def printMenu(path_to_menu,db):
    indices = parseMenu(path_to_menu)
    for index in indices:
        print '==============================='
        print db[index]['NAME']
        print '-------------------------------'
        for i in db[index]['INGREDIENTS']:
            print i['QUANTITY'], i['MEASUREMENT'], i['DESCRIPTION'], i['DIRECTION']
        print '-------------------------------'
        print db[index]['DIRECTIONS']
    print '==============================='

def assign_recipe_ids(db):
    for r in db:
        id = r.get('RECIPE_ID', None)
        if not id:
            r['RECIPE_ID'] = str(uuid.uuid4())


db=plistlib.readPlist(FILE_PATH)

argparser = argparse.ArgumentParser(description="Command line recipe tool.")
argparser.add_argument('-r','--recipes', dest='print_all_recipes', action='store_true',
                       help='print a list of all recipes')
argparser.add_argument('-c','--custom', dest='custom', action='store_true',
                       help='custom operation, changes frequently')
argparser.add_argument('-s','--shoppinglist', dest='selected_recipes', action='store',
                       type=argparse.FileType('r'),
                       help='read in a file with selected recipes marked with "y " at the start of line and generate shopping list')
args = argparser.parse_args()

if args.print_all_recipes:
    printNames(db)
elif args.selected_recipes:
    printMenu(args.selected_recipes,db)
elif args.custom:
    plistlib.writePlist({'RECIPES': db}, FILE_PATH)
