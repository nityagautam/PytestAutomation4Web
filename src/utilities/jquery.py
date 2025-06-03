class jQuery():
    def __init__(self, selector):
        self.selector = selector
        self.methods = []

    def __str__(self):
        command = "window.jQuery(\"%s\", window.document)" % self.selector
        for method in self.methods:
            command = command + method

        return command

    def parent(self, selector=None):
        if selector is not None:
            self.methods.append(".parent(\"%s\")" % selector)
        else:
            self.methods.append(".parent()")

        return self

    def children(self, selector=None):
        if selector is not None:
            self.methods.append(".children(\"%s\")" % selector)
        else:
            self.methods.append(".children()")

        return self

    def next(self):
        self.methods.append(".next()")

        return self

    def prev(self):
        self.methods.append(".prev()")

        return self

    def hide(self):
        self.methods.append(".hide()")

        return self

    def show(self):
        self.methods.append(".show()")

        return self

    def eq(self, index):
        self.methods.append(".eq(%s)" % index)

        return self

    def text(self):
        self.methods.append(".text()")

        return self

    def attr(self, attribute):
        self.methods.append(".attr(\"%s\")" % attribute)

        return self

    @property
    def length(self):
        self.methods.append(".length")

        return self