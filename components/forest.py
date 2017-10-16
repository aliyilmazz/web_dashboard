class forest:
    _attributes = {}
    def description(self):
        """
        description returns a string describing what component does.
        """
        return "This, is, FOREST !! !!! !"
    def getitem(self, index):
        """
        fetches the value from they key whose index is given as
        the second parameter.
        """
        return self._attributes[index]
    def setitem(self, index, value):
        """
        assigns given value to the corresponding key in the attribute
        dictionary regarding the given index.
        """
        self._attributes[index] = value
    def attributes(self):
        """
        attributes returns a list of attribute names and types for the component. Attributes are used
        at design time to configure a components behaviour.
        """
        retlist = []
        for attr in self._attributes:
            retlist.append((attr,self._attributes[attr]))
        return retlist
    def methods(self):
        """
        methods return a list of method calls and their descriptions. The methods define the behaviour
        of the component at execution time. This way, application can interact with the components
        	"""
        methods_list = []
        for x in dir(self):
            if type(getattr(self, x)).__name__ == 'instancemethod':
                methods_list.append((x, getattr(self,x).__doc__))
        return methods_list
    def execute(self):
        """
        execute method will result in execution of component body. Result depends on the component
        type. A web application can generate HTML content where a graph based component gets
        all of inputs and generate outputs.
        execute is the basic behaviour of the component on execution time. The application is
        expected to call execute method of all added components to execute a design.
        """
        return """<img width="100%" height="auto" src="https://static.pexels.com/photos/4827/nature-forest-trees-fog.jpeg" alt="Forest of the Day"><p>A Forest A Day Keeps STRESS away</p>"""
