class Category:

    def __init__(self, name):
        self.name = name
        self.recipes = []

    def __repr__(self):
        return '%s (%d)' % (self.name, len(self.recipes))