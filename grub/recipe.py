# class Recipe:
	
# 	def __init__(self, data):
#         self.data = data

#     def get_id(self):
#         return self.data['RECIPE_ID']

#     def get_name(self):
#         return self.data['NAME']

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