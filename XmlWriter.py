from xml.dom import minidom
from xml.etree import ElementTree


class XmlWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write_tree(self, tree: ElementTree.Element):
        """ writes xml to an output file using the element tree. """
        xmlstr = ElementTree.tostring(tree, encoding='utf8', method='html').decode("utf8")
        xmlstr = minidom.parseString(xmlstr).toprettyxml()
        xmlstr = xmlstr.replace("<parameterList/>", "<parameterList>\n</parameterList>")
        xmlstr = xmlstr.replace("<expressionList/>", "<expressionList>\n</expressionList>")
        xmlstr = xmlstr.replace("\t", "  ")
        xmlstr = xmlstr.replace('<?xml version="1.0" ?>\n', "")
        self.output_file.write(xmlstr)
