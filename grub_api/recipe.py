from grub_api.utils import SubHeading

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
        values.extend(['', '%s' % self.directions.encode('utf8')])
        return '\n'.join(values)