import argparse

from grub.database import Database
from grub.text_interface import TextInterface

argparser = argparse.ArgumentParser(description="Command line to interact with the Grub database.")
argparser.add_argument('grub_file', help='The grub file to read from')
argparser.add_argument('-c','--category_edit', dest='edit_categories', action='store_true',
                       help='Edit the existing categories')

args = argparser.parse_args()

grub_db = Database(file_path=args.grub_file)
ti = TextInterface()

all_categories = grub_db.categories
if args.edit_categories:
    for c in all_categories:
        ti.append("- %s" % c.name)
    ti.append("")
    ti.append("=================================")

    category_prefix = "-" * len(all_categories)
    for c in all_categories:
        for r in c:
            ti.append(category_prefix + r.name)
    
    ti.run()
    for line in ti.get_line():
        print '>', line

