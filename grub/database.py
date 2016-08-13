import plistlib

class Database:
    
    # from grub.database import Database
    # myDB = Database()
    # myDB.import_macgourmet('/path/to/macgourmet.export')
    # myDB.save('/path/to/grub.plist')
    # myDB.open('/path/to/grub.plist')
    
    COLLECTIONS_KEY = 'COLLECTIONS'
    RECIPES_KEY = 'RECIPES'

    def __init__(self):
        self.db = {}
        self.db[Database.COLLECTIONS_KEY] = []
        self.db[Database.RECIPES_KEY] = []

    def collections(self):
        return self.db[Database.COLLECTIONS_KEY]

    def recipes(self):
        return self.db[Database.RECIPIES_KEY]

    def import_macgourmet(self, path):
        '''IMPLEMENT'''
        pass

    def save(self, path):
        plistlib.writePlist(self.db, path)

    def open(self, path):
        self.db = plistlib.readPlist(path)