# class Recipe:
#     def print_recipe(self):
#     	print '==============================='
#         print self.get_name()
#         print '-------------------------------'
#         for i in self.data['INGREDIENTS']:
#             print i['QUANTITY'], i['MEASUREMENT'], i['DESCRIPTION'], i['DIRECTION']
#         print '-------------------------------'
#         print self.data['DIRECTIONS']
#         print '==============================='

class Recipe:

    def __init__(self, name, **kwargs):
        self.name = name
        self.directions = kwargs['directions'] if 'directions' in kwargs else ""
        self.ingredients = kwargs['ingredients'] if 'ingredients' in kwargs else []
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.location = kwargs['location'] if 'location' in kwargs else ""
        