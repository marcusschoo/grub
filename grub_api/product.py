class Ingredient:

    def __init__(self, product, amount=None, unit=None):
        self.product = product
        self.amount = amount
        self.unit = unit
        #validate unit against product measure

    def __repr__(self):
        return '%s%s%s' % \
        ('%g ' % self.amount if self.amount else '', \
         '%s ' % self.unit if self.unit else '', \
         self.product.name)

class Product:

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
    
    def __init__(self, name):
        self.name = Product.get_sanitised_name(name)
        if not self.name:
            raise ValueError("%s is invalid product name." % name)
        self.id = None
        self.category = None

    @staticmethod
    def get_sanitised_name(name):
        sanitised_name = name.lower().strip()
        if sanitised_name in Product.sanitised_name_map:
            sanitised_name = Product.sanitised_name_map[sanitised_name]
        if sanitised_name.endswith(" tablespoons oil"): 
            sanitised_name = "oil, canola"
        return sanitised_name
