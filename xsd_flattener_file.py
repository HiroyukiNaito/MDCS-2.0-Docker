    
"""XSD Flattener File class
"""
import os
from xml_utils.xsd_flattener.xsd_flattener import XSDFlattener


class XSDFlattenerFile(XSDFlattener):
    """XSD Flattener class getting dependencies by URL
    """

    def __init__(self, xml_string):
        """ Initialize the flattener
        Args:
            xml_string:
        """
        XSDFlattener.__init__(self, xml_string=xml_string)

    def get_dependency_content(self, uri):
        """ Opne the content found at the URI
        Args:
            uri:
        Returns:
        """
        content = ""
        path = '/srv/mgi-mdcs/modular-data-models-include/' + uri
        file = open(path, 'r')
        content  = file.read()

        return content
