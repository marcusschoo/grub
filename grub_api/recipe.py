from grub_api.utils import SubHeading
from grub_api.product import Ingredient
from grub_api.product import Product

class Recipe:

    def __init__(self, name, **kwargs):
        self.name = name.title()
        self.directions = kwargs['directions'] if 'directions' in kwargs else ""
        self.ingredients = kwargs['ingredients'] if 'ingredients' in kwargs else []
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.location = kwargs['location'] if 'location' in kwargs else ""
    
    def __repr__(self):
        values = ['%s\n' % SubHeading(self.name)]
        if self.location:
            values.append('Location: %s\n' % self.location)
        values.extend(['%s' % i for i in self.ingredients])
        if isinstance(self.directions, unicode):
            directions = '%s' % self.directions.encode('utf8')
        else:
            directions = self.directions
        values.extend(['', directions])
        return '\n'.join(values)

    @staticmethod
    def get_recipe_template():
        n = 'Recipe Name'
        l = 'Recipe Location'
        d = 'First Recipe Direction\nSecond Recipe Direction'
        p = [Product('Product A'), Product('Product B')]
        i = [Ingredient(a,1,'unit') for a in p]
        return Recipe(n, location=l, directions=d, ingredients=i)