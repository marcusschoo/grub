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

    def __init__(self, name, directions):
        self.name = name
        self.directions = directions
        self.ingredients = []
        self.id = None
        self.location = ""
        