

class Heading:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '%s\n%s\n' % (self.text, '=' * len(self.text))

class SubHeading:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '%s\n%s' % (self.text, '-' * len(self.text))