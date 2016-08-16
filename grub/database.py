import plistlib
import os.path

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

    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.db = plistlib.readPlist(path)
        else:
            self.db = {}
            self.db[Database.COLLECTIONS_KEY] = []
            self.db[Database.RECIPES_KEY] = []

    def recipes(self):
        return self.db[Database.RECIPES_KEY]

    def save_recipe(self, recipe):
        recipe_data = {}
        recipe_data[Database.RECIPE_NAME_KEY] = recipe.name
        recipe_data[Database.RECIPE_DIRECTIONS_KEY] = recipe.directions
        self.recipes().append(recipe_data)
        self.save()

    def save(self):
        plistlib.writePlist(self.db, self.file_path)