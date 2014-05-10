from xml.etree import ElementTree



class XMLResult:
	def __init__(self, xmlfile):
		'''Grab lat and long from XML and return it'''
		self.tree = ElementTree.parse(xmlfile)
		self.root = self.tree.getroot()
		self.lat = ''
		self.lng = ''
		for child in self.root:
			if child.tag == "result":
				self.child = child
		for subchild in self.child:
			if subchild.tag == "geometry":
				self.geometryTag = subchild
		for child in self.geometryTag:
			if child.tag == "location":
				for subchild in child:
					if self.lat == '':
						self.lat = subchild.text
					else:
						self.lng = subchild.text
		print "Latitude: "+self.lat+'\n', "Longitude: "+self.lng+'\n'
							
