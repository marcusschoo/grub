import plistlib
import os.path
import uuid

from grub.product import Product
# class Database:
    
#     # from grub.database import Database
#     # myDB = Database()
#     # myDB.import_macgourmet('/path/to/macgourmet.export')
#     # myDB.save('/path/to/grub.plist')
#     # myDB.open('/path/to/grub.plist')
    
#     COLLECTIONS_KEY = 'COLLECTIONS'
#     RECIPES_KEY = 'RECIPES'

#     def __init__(self):
#         self.db = {}
#         self.db[Database.COLLECTIONS_KEY] = []
#         self.db[Database.RECIPES_KEY] = []

#     def collections(self):
#         return self.db[Database.COLLECTIONS_KEY]

#     def recipes(self):
#         return self.db[Database.RECIPIES_KEY]

#     def import_macgourmet(self, path):
#         '''IMPLEMENT'''
#         pass

#     def save(self, path):
#         plistlib.writePlist(self.db, path)

#     def open(self, path):
#         self.db = plistlib.readPlist(path)

class Database:
    
    COLLECTIONS_KEY = 'COLLECTIONS'
    RECIPES_KEY = 'RECIPES'
    RECIPE_NAME_KEY = 'RECIPE_NAME'
    RECIPE_DIRECTIONS_KEY = 'RECIPE_DIRECTIONS'
    RECIPE_ID_KEY = 'RECIPE_ID'
    RECIPE_LOCATION_KEY = 'RECIPE_LOCATION'
    PRODUCTS_KEY = 'PRODUCTS'
    PRODUCT_NAME_KEY = 'PRODUCT_NAME'
    PRODUCT_ID_KEY = 'PRODUCT_ID'
    
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.db = plistlib.readPlist(file_path)
        else:
            self.db = {}
            self.db[Database.COLLECTIONS_KEY] = []
            self.db[Database.RECIPES_KEY] = []
            self.db[Database.PRODUCTS_KEY] = []

    def _recipes(self):
        return self.db[Database.RECIPES_KEY]

    def _products(self):
        return self.db[Database.PRODUCTS_KEY]

    def recipe_exists(self, recipe):
        if recipe.id:
            for r in self._recipes():
                if r.id == recipe.id:
                    return True
        return False

    def _add_recipe(self, recipe):
        recipe.id = str(uuid.uuid4())
        recipe_data = {}
        recipe_data[Database.RECIPE_NAME_KEY] = recipe.name
        recipe_data[Database.RECIPE_DIRECTIONS_KEY] = recipe.directions
        recipe_data[Database.RECIPE_ID_KEY] = recipe.id
        recipe_data[Database.RECIPE_LOCATION_KEY] = recipe.location
        self._recipes().append(recipe_data)

    def _update_recipe(self, recipe):
        raise NotImplementedError('Updating recipe not supported')
        
    def save_recipe(self, recipe):
        if self.recipe_exists(recipe):
            self._update_recipe(recipe)
        else:
            self._add_recipe(recipe)
        self._save()

    def find_product_by_name(self, name):
        sanitised_name = Product.get_sanitised_name(name)
        products = [p for p in self._products() if p[Database.PRODUCT_NAME_KEY] == sanitised_name]
        if len(products) > 1:
            raise Exception("Found %d products matching the name %s" % (len(products), name))
        return products[0] if products else None

    def _add_product(self, product):
        product.id = str(uuid.uuid4())
        product_data = {}
        product_data[Database.PRODUCT_NAME_KEY] = product.name
        product_data[Database.PRODUCT_ID_KEY] = product.id
        self._products().append(product_data)
        
    def save_product(self, product):
        self._add_product(product)
        self._save()
    
    def _save(self):
        plistlib.writePlist(self.db, self.file_path)