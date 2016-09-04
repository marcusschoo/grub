import plistlib
import os.path
import uuid

from grub_api.product import Product
from grub_api.category import Category
from grub_api.recipe import Recipe
from grub_api.product import Ingredient

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
        self.id_to_product_map = {}
        self.id_to_recipe_map = {}
        self.categories = []

        if os.path.exists(file_path):
            db = plistlib.readPlist(file_path)
            self._deserialise_products(db[Database.PRODUCTS_KEY])
            self._deserialise_recipes(db[Database.RECIPES_KEY])
            self._deserialise_categories(db[Database.CATEGORIES_KEY])

    @property
    def recipes(self):
        return self.id_to_recipe_map.values()

    @property
    def recipe_ids(self):
        return self.id_to_recipe_map.keys()

    def _deserialise_products(self, product_data):
        for p in product_data:
            try:
                grub_product = Product(p[Database.PRODUCT_NAME_KEY])
                grub_product.id = p[Database.PRODUCT_ID_KEY]
                self.id_to_product_map[grub_product.id] = grub_product
            except:
                pass

    def _deserialise_recipes(self, recipe_data):
        for r in recipe_data:
            grub_recipe = Recipe(r[Database.RECIPE_NAME_KEY], 
                location=r[Database.RECIPE_LOCATION_KEY],
                id = r[Database.RECIPE_ID_KEY],
                directions=r[Database.RECIPE_DIRECTIONS_KEY])
            for i in r[Database.RECIPE_INGREDIENTS_KEY]:
                grub_product = self.find_product_by_id(i[Database.PRODUCT_ID_KEY])
                if grub_product:
                    grub_recipe.ingredients.append(Ingredient(grub_product,
                        i.get(Database.INGREDIENT_AMOUNT_KEY, None),
                        i.get(Database.INGREDIENT_UNIT_KEY, None)))
            self.id_to_recipe_map[grub_recipe.id] = grub_recipe

    def _deserialise_categories(self, category_data):
        for c in category_data:
            grub_category = Category(c[Database.CATEGORY_NAME_KEY])
            for r in c[Database.CATEGORY_RECIPES_KEY]:
                grub_recipe = self.find_recipe_by_id(r)
                if grub_recipe:
                    grub_category.recipes.append(grub_recipe)
                else:
                    raise KeyError('Recipe in category %s not found.' % grub_category.name)
            self.categories.append(grub_category)

    def _serialise_products(self):
        product_list = []
        for p in sorted(self.id_to_product_map.values(), key=lambda p: p.name):
            product_data = {}
            product_data[Database.PRODUCT_NAME_KEY] = p.name
            product_data[Database.PRODUCT_ID_KEY] = p.id
            product_list.append(product_data)
        return product_list

    def _serialise_recipes(self):
        recipe_list = []
        for recipe in sorted(self.id_to_recipe_map.values(), key=lambda recipe: recipe.name):
            recipe_data = {}
            recipe_data[Database.RECIPE_NAME_KEY] = recipe.name
            recipe_data[Database.RECIPE_DIRECTIONS_KEY] = recipe.directions
            recipe_data[Database.RECIPE_ID_KEY] = recipe.id
            recipe_data[Database.RECIPE_LOCATION_KEY] = recipe.location

            recipe_ingredients = []
            for i in recipe.ingredients:
                data = {Database.PRODUCT_ID_KEY: i.product.id}
                if i.amount:
                    data[Database.INGREDIENT_AMOUNT_KEY] = i.amount
                if i.unit:
                    data[Database.INGREDIENT_UNIT_KEY] = i.unit
                recipe_ingredients.append(data)

            recipe_data[Database.RECIPE_INGREDIENTS_KEY] = recipe_ingredients
            recipe_list.append(recipe_data)
        return recipe_list

    def _serialise_categories(self):
        category_list = []
        for category in sorted(self.categories, key=lambda category: category.name):
            category_data = {}
            category_data[Database.CATEGORY_NAME_KEY] = category.name
            recipe_ids = []
            for r in category.recipes:
                recipe_ids.append(r.id)
            category_data[Database.CATEGORY_RECIPES_KEY] = recipe_ids
            category_list.append(category_data)
        return category_list
        
    def save(self, file_path):
        db = {}
        db[Database.CATEGORIES_KEY] = self._serialise_categories()
        db[Database.RECIPES_KEY] = self._serialise_recipes()
        db[Database.PRODUCTS_KEY] = self._serialise_products()

        plistlib.writePlist(db, file_path)

    def find_product_by_id(self, product_id):
        return self.id_to_product_map[product_id] if product_id in self.id_to_product_map else None

    def find_recipe_by_id(self, recipe_id):
        return self.id_to_recipe_map[recipe_id] if recipe_id in self.id_to_recipe_map else None

    def find_product_by_name(self, name):
        sanitised_name = Product.get_sanitised_name(name)
        products = [p for p in self.id_to_product_map.values() if p.name == sanitised_name]
        if len(products) > 1:
            raise Exception("Found %d products matching the name %s" % (len(products), name))
        
        return products[0] if products else None

    def find_recipe_by_name(self, name):
        recipes = [r for r in self.id_to_recipe_map.values() if r.name == name]
        if len(recipes) > 1:
            raise Exception("Found %d recipes matching the name %s" % (len(recipes), name))
        
        return recipes[0] if recipes else None

    def find_category_by_name(self, name):
        categories = [c for c in self.categories if c.name == name]
        if len(categories) > 1:
            raise Exception("Found %d categories matching the name %s" % (len(categories), name))
        
        return categories[0] if categories else None

    # def update_recipe(self, recipe):
    #     self.id_to_recipe_map[recipe.id] = recipe
        
    def add_recipe(self, recipe):
        existing_recipe = self.find_recipe_by_id(recipe.id)
        if existing_recipe:
            raise RuntimeError("The recipe already exists")
        recipe.id = str(uuid.uuid4())
        self.id_to_recipe_map[recipe.id] = recipe

    def add_product(self, product):
        existing_product = self.find_product_by_id(product.id)
        if existing_product:
            raise RuntimeError("The product already exists")
        product.id = str(uuid.uuid4())
        self.id_to_product_map[product.id] = product
        
    def add_category(self, category):
        existing_categories = [c for c in self.categories if c.name == category.name]
        if existing_categories:
            raise RuntimeError("Category %s already exists" % category.name)
        self.categories.append(category)






