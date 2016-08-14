from grub.recipe import Recipe

class RecipeCollection:
	def __init__(self, data):
        self.data = data
        self.recipe_list = []

    def get_id(self):
        return self.data['COLLECTION_ID']

    def get_name(self):
        return self.data['NAME']

    def get_recipes(self):
    	if not self.recipe_list:
    		for r in self.data['RECIPES']:
    			self.recipe_list.append(Recipe(r))
    	return self.recipe_list
