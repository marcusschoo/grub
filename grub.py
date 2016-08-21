#!/usr/bin/python

import argparse

from grub.database import Database
from grub.category import Category

argparser = argparse.ArgumentParser(description="Command line to interact with the Grub database.")
argparser.add_argument('grub_file', help='The grub file to read from')
argparser.add_argument('-c','--category_edit', dest='edit_categories', action='store_true',
                       help='Edit the existing categories')
argparser.add_argument('-C','--category_new', dest='new_category', action='store',
                       help='Create a new category.')

args = argparser.parse_args()

grub_db = Database(file_path=args.grub_file)

if args.edit_categories:
    for c in grub_db.categories:
        print c
elif args.new_category:
	grub_category = Category(args.new_category)
	grub_db.save_category(grub_category)