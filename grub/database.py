import plistlib
import os.path
import uuid

from grub.product import Product
from grub.category import Category
from grub.recipe import Recipe

class Database:
    
    CATEGORIES_KEY = 'CATEGORIES'
    CATEGORY_NAME_KEY = 'CATEGORY_NAME'
    CATEGORY_RECIPES_KEY = 'CATEGORY_RECIPES'
    RECIPES_KEY = 'RECIPES'
    RECIPE_NAME_KEY = 'RECIPE_NAME'
    RECIPE_DIRECTIONS_KEY = 'RECIPE_DIRECTIONS'
    RECIPE_ID_KEY = 'RECIPE_ID'
    RECIPE_LOCATION_KEY = 'RECIPE_LOCATION'
    RECIPE_INGREDIENTS_KEY = 'RECIPE_INGREDIENTS'
    PRODUCTS_KEY = 'PRODUCTS'
    PRODUCT_NAME_KEY = 'PRODUCT_NAME'
    PRODUCT_ID_KEY = 'PRODUCT_ID'
    INGREDIENT_AMOUNT_KEY = 'INGREDIENT_AMOUNT'
    INGREDIENT_UNIT_KEY = 'INGREDIENT_UNIT'
    
    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.db = plistlib.readPlist(file_path)
        else:
            self.db = {}
            self.db[Database.CATEGORIES_KEY] = []
            self.db[Database.RECIPES_KEY] = []
            self.db[Database.PRODUCTS_KEY] = []

    @property
    def categories(self):
        category_list = []
        for c in self.db[Database.CATEGORIES_KEY]:
            the_category = Category(c[CATEGORY_NAME_KEY])
            for r in c[CATEGORY_RECIPES_KEY]:
                the_category.recipes.append(Recipe(r[Database.RECIPE_NAME_KEY], id=r[Database.RECIPE_ID_KEY]))
            category_list.append(the_category)
        return category_list

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

        recipe_ingredients = []
        for i in recipe.ingredients:
            recipe_ingredients.append({Database.PRODUCT_ID_KEY: i.product.id,
                                       Database.INGREDIENT_AMOUNT_KEY: i.amount,
                                       Database.INGREDIENT_UNIT_KEY: i.unit})

        recipe_data[Database.RECIPE_INGREDIENTS_KEY] = recipe_ingredients
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
        grub_product = None
        sanitised_name = Product.get_sanitised_name(name)
        products = [p for p in self._products() if p[Database.PRODUCT_NAME_KEY] == sanitised_name]
        if len(products) > 1:
            raise Exception("Found %d products matching the name %s" % (len(products), name))
        if products:
            grub_product = Product(products[0][Database.PRODUCT_NAME_KEY])
            grub_product.id = products[0][Database.PRODUCT_ID_KEY]
        return grub_product

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