class ShoppingList:

    # from grub.shopping_list import ShoppingList
    # my_shopping_list = ShoppingList(db)
    # my_shopping_list.generate_form()
    # my_shopping_list.read_form()
    # my_shopping_list.generate_menu()
    # my_shopping_list.generate_shopping_list()

    def __init__(self, db):
        self.db = db

    def generate_form(self):
        for c in self.db.collections():
            print '#', c.get_name()
            for r in c.get_recipes():
                print r.get_name()

    def read_form(self):
        pass

    def generate_menu(self, selected_recipes):
        for r in selected_recipes:
            r.print_recipe()

    def generate_shopping_list(self):
        pass
