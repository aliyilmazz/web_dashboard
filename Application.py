#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
from imp import load_source


def css_link(filename):
	return """<link rel="stylesheet" href="./components/%s.css">\n""" % filename


def html_column(content, width):
	width = 100.0 / width
	return """\t\t\t<div class="column" style="width: %.2f%%">%s</div>\n""" % (width, content)


# Base container class, Application
class Application():
	"""
	Application class is the container of all components. It allows user to search, add, remove
	components in the design mode. Later, it executes the components to form collective behaviour.
	"""

	def __init__(self):
		"""
		Constructor for the Application class.
		"""
		self._componentsFolder = "./components"
		self._designsFolder = "./designs"
		self._loadedComponents = {}
		self._instances = {}

	def available(self):
		"""
		Lists the names of the available components. Application has a directory path containing
		python module files for the components. available method return list of such components at
		run-time. Components can be installed even after the application started.
		A sample output could be [’rss’,’mblog’] indicating rss.py and mblog.py exists in the component
		directory.
		"""
		return [path.basename(f)[:path.basename(f).find(".py")] for f in glob(self._componentsFolder + "/*.py")]

	def loaded(self):
		"""
		Returns a dictionary of the names and descriptions of the loaded components.
		A sample output could be {’rss’:’RSS reader’,’mblog’:’A tiny microblog’}. Application can add
		instances of loaded components.
		"""
		loaded_dict = {}
		for component in self._loadedComponents:
			loaded_dict[component] = self._loadedComponents[component]().description()
		return loaded_dict

	def load(self, component):
		"""
		load() is similar to Python import however it searches the module in component path. It keeps
		track of the component loaded and the class implementing the component so that instances
		can be created.
		"""
		if component not in self._loadedComponents:
			component_class = getattr(load_source(component, self._componentsFolder + "/" + component + ".py"), component)
			self._loadedComponents[component] = component_class
		return self._loadedComponents[component]

	def loadDesign(self, design_string):
		"""
		A design can be loaded from a file. The file format depends on you.
		Loading a design should load() all required components and create all instances with their configured
		attributes.
		"""
		self._instances = {}
		for line in [x for x in design_string.split("\n") if x != '']:
			instance_id, component_name, x, y = line.split(" ")
			self.load(component_name)
			self._instances[instance_id] = (self._loadedComponents[component_name](), (int(x), int(y)))
		return "successfully loaded design " + design_string

	def saveDesign(self):
		"""
		A design can be saved to a file. The file format depends on you.
		"""
		design_string = ""
		for instance in self._instances:
			design_string += instance + " " + self._instances[instance][0].__module__ + " " + \
			str(self._instances[instance][1][0]) + " " + str(self._instances[instance][1][1]) + "\n"
		return design_string

	def addInstance(self, component_name, x, y):
		"""
		creates an instance from a loaded component and places it on given coordinates.
		The coordinates can be on a grid, on a column or row layout. x and y parameters can be
		modified or new parameters can be added as you need.
		addInstance returns a string id for the created component instance. Later calls
		refer to this id when they need to access the component.
		"""
		from random import randint
		while True:
			instance_id = ""
			for i in range(8):
				instance_id += chr(randint(ord('0'), ord('z')))
			if instance_id not in self._instances:
				break
		self._instances[instance_id] = (self._loadedComponents[component_name](), (x, y))
		return instance_id

	def instances(self):
		"""
		instances returns the current set of components in the application as a dictionary. The returned
		dictionary has the component instance id as the key and component name and its
		position in a tuple as the value.
		"""
		instances = {}
		for instance in self._instances:
			instances[instance] = (self._instances[instance][0].__module__, self._instances[instance][1])
		return instances

	def removeInstance(self, instance_id):
		"""
		removes a component instance from the current design.
		"""
		self._instances.__delitem__(instance_id)
		return "removed instance", instance_id

	def callMethod(self, instance_id, method_name, *params):
		"""
		This method is used by application to call methods of the component instances.
		callMethod(’rss1231’,’refresh’,None) calls refresh () of the identified RSS component.
		"""
		comp_instance = self._instances[instance_id][0]  # both the class name and the file name
		getattr(comp_instance, method_name)(*params)
		return "called " + method_name + " of instance " + instance_id + " with parameters " + params

	def execute(self):
		"""
		This is the application execution mode. It executes all added component instances and
		generate the collective result. In web project it can be the whole HTML page. In graph based
		projects it is the graph traversal resulting in the whole application action.
		"""
		template = open("template.html", "r")
		result = open("index.html", "w+")
		maxX, maxY = -1, -1
		continue_flag = False

		# get max x and max y
		for instance in self._instances:
			if self._instances[instance][1][0] > maxX: maxX = self._instances[instance][1][0]
			if self._instances[instance][1][1] > maxY: maxY = self._instances[instance][1][1]

		# fill index.html file
		for line in template:
			if line.find("%%cssfiles") > -1:
				for component in self.loaded():
					result.write("\t\t" + css_link(component))
			elif line.find("%%content") > -1:
				for j in range(maxY + 1):
					# prepare html row
					row_content = ""
					for i in range(maxX + 1):
						for instance in self._instances:
							if self._instances[instance][1][0] == i \
									and self._instances[instance][1][1] == j:
								row_content += html_column(self._instances[instance][0].execute(), maxX + 1)
								# this cell is now filled. continue with the next cell
								continue_flag = True
								break
						if continue_flag:
							continue_flag = False
							continue
						row_content += html_column("<h1>empty</h1>", maxX + 1)
					result.write("""\t\t<div class="row">\n%s\t\t</div>\n""" % row_content)
			else:
				result.write(line)

		result.close()
		template.close()

		return "successfully executed application."


# In case Application is executed as a stand-alone script
if __name__ == '__main__':
	app = Application()
	app.loadDesign("./designs/myUniqueDesign")
	app.execute()
