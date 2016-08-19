import plistlib
import os.path
import uuid

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

    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.db = plistlib.readPlist(file_path)
        else:
            self.db = {}
            self.db[Database.COLLECTIONS_KEY] = []
            self.db[Database.RECIPES_KEY] = []

    def recipes(self):
        return self.db[Database.RECIPES_KEY]

    def recipe_exists(self, recipe):
        if recipe.id:
            for r in self.recipes():
                if r.id == recipe.id:
                    return True
        return False

    def add_recipe(self, recipe):
        recipe_data = {}
        recipe_data[Database.RECIPE_NAME_KEY] = recipe.name
        recipe_data[Database.RECIPE_DIRECTIONS_KEY] = recipe.directions
        recipe_data[Database.RECIPE_ID_KEY] = str(uuid.uuid4())
        recipe_data[Database.RECIPE_LOCATION_KEY] = recipe.location
        self.recipes().append(recipe_data)

    def update_recipe(self, recipe):
        raise NotImplementedError('Updating recipe not supported')
        
    def save_recipe(self, recipe):
        if self.recipe_exists(recipe):
            self.update_recipe(recipe)
        else:
            self.add_recipe(recipe)
        self.save()

    def save(self):
        plistlib.writePlist(self.db, self.file_path)