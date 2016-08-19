import plistlib
import argparse

from grub.recipe import Recipe
from grub.database import Database

sanitised_name_map = {
"aubergine (egg plant)": "eggplant", \
"average pears": "pear", \
"baking soda": "baking powder", \
"basil leaves": "basil", \
"berries, blue": "blueberries", \
"butter, unsalted": "butter", \
"capsicum, greem": "capsicum, green", \
"carbohydrate": "", \
"carrot": "carrots", \
"cayenne powder": "chilli powder", \
"cheese, grated": "cheese, edam", \
"chilli, ground": "chilli powder", \
"chopped mushrooms": "mushrooms", \
"cold rice": "rice", \
"coriander, dried": "coriander, leaves", \
"corn, kernels": "corn, frozen", \
"cornstarch": "corn starch", \
"cottage cheese": "cheese, cottage", \
"courgette": "zucchini", \
"dried hazelnuts": "hazelnuts", \
"egg": "eggs", \
"energy": "", \
"fat": "", \
"feta": "cheese, feta", \
"flour": "flour, plain", \
"fresh coriander leaves": "coriander, fresh", \
"fresh wholemeal breadcrumbs": "breadcrumbs", \
"frozen vege sausages": "sausages", \
"granulated sugar": "sugar", \
"grated carrot": "carrots", \
"ground cumin": "cumin, ground", \
"haloumi": "cheese, haloumi", \
"kalamata olives": "olives, kalamata", \
"large eggplant": "eggplant", \
"lemon juice": "juice, lemon", \
"mango chutney to serve": "", \
"medium onion": "onion, brown", \
"medium tomatoes": "tomatoes", \
"milk, butter": "buttermilk", \
"mozzarella": "cheese, mozzarella balls", \
"mushrooms, field": "mushrooms, portabello", \
"nut, pea": "peanuts", \
"nuts, cashew": "nut, cashew", \
"oak leaf lettuce leaves": "lettuce", \
"oil (canola or vegetable)": "oil, canola", \
"olive oil": "oil, olive", \
"olive, black": "olives, black", \
"olive, green": "olives, green", \
"olive": "olives, black", \
"olive, kalamata": "olives, kalamata", \
"onion": "onion, brown", \
"packages halloumi cheese": "cheese, halloumi", \
"orzo pasta": "pasta, orzo", \
"parsley": "parsley, dried", \
"pasta spirals": "pasta, spiral", \
"peas": "peas, frozen", \
"penne, cooked": "pasta, penne", \
"penne, dried tomato-basil": "pasta, penne", \
"protein": "", \
"pita bread": "tortillas", \
"ripe tomatoes": "tomatoes", \
"rolls": "breadrolls", \
"salt and pepper": "salt & pepper", \
"salt (optional)": "salt", \
"sambal oelek": "chilli paste", \
"small tortillas": "tortillas", \
"spinach, fresh baby leaves": "spinach, fresh", \
"spinach, baby leaf": "spinach, fresh", \
"spinach, chopped": "spinach, fresh", \
"spring onions": "onion, spring", \
"squash (e.g. zucchini)": "zucchini", \
"sunflower seeds": "seeds, sunflower", \
"taco shells": "tortillas", \
"three bean mix": "beans, three bean mix", \
"toasted breadcrumbs": "breadcrumbs", \
"tofu, firm": "tofu", \
"tomato": "tomatoes", \
"tomato pasta sauce": "pasta sauce", \
"tomato paste": "tomato, paste", \
"vegie delights": "sausages", \
"water, cold": "water", \
"wholemeal flat rolls": "breadrolls" \
}

# mace??
# quinoa cooked
# first and second mixture
# spinach chopped
# stove
# tent pegs
# unbaked pie crust

def sanitise_product_name(name):
    sanitised_name = name.lower().strip()
    if sanitised_name in sanitised_name_map:
        sanitised_name = sanitised_name_map[sanitised_name]
    if sanitised_name.endswith(" tablespoons oil"):
        sanitised_name = "oil, canola"
    return sanitised_name

argparser = argparse.ArgumentParser(description="Command line to convert macgourmet export plist to Grub.")
argparser.add_argument('macgourmet_file',
                       help='The macgourmet recipe export to convert')
args = argparser.parse_args()

if args.macgourmet_file:
    print 'Checking ingredients in', args.macgourmet_file
    macgourmet_data = plistlib.readPlist(args.macgourmet_file)
    products = set()
    for mg_recipe in macgourmet_data:
        products.update([sanitise_product_name(i['DESCRIPTION']) for i in mg_recipe['INGREDIENTS']])

    print len(products)
    print "\n".join(sorted(list(products)))

print 'Done'