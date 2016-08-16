import grub

class Recipe:

	def __init__(self, name, directions):
		self.name = name
		self.directions = directions
		self.ingredients = []
		self.id = None

class Product:

	def __init__(self, name, measure=Measure.kVolume):
		self.name = name
		self.measure = measure
		self.id = None
		self.category = 'tins'

class Store:

	def __init__(self, name):
		self.name = name
		self.category_order = ['fresh produce','tins','freezer']

class Measure:

	def __init__(self):
		self.kVolume = 0
		self.kWeight = 1
		self.kUnits = 2

class Ingredient:

	def __init__(self, product, amount, unit=kCup):
		self.product = product
		self.amount = amount
		self.unit = unit
		#validate unit against product measure

grub_db = grub.read('path/grub.plist')

new_recipe = Recipe(name='foo', directions='something')
grub_db.save_recipe(new_recipe)
# info: new recipe created
cumin = grub_db.get_product_by_name('cumin')
if not cumin:
	cumin = Product('cumin', kVolume)
	grub_db.save_product(cumin)
new_recipe.add_ingredient(Ingredient(cumin, 1, Unit.kTsp))
grub_db.save_recipe(new_recipe)
# info: recipe updated

new_recipe = Recipe(name='foo', directions='something')
new_recipe.add_ingredient(Ingredient(grub_db.get_product_by_name('cumin'), 1, Unit.kTsp))
grub_db.save_recipe(new_recipe)
# info: recipe saved
