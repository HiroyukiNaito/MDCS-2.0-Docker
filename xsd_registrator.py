"""
Importing XSD template for MDCS
"""
import HTMLParser
import json
import glob
import os
import django
import xml.dom.minidom

django.setup()

from logging import getLogger
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_composer_app.components.type.models import Type
from core_composer_app.components.type_version_manager import api as type_version_manager_api
from core_composer_app.components.type_version_manager.models import TypeVersionManager
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import NotUniqueError
from xsd_flattener_file import XSDFlattenerFile

logger = getLogger("xsd_registrator.py")


def _set_xsd_template(xsd_filename, xsd_data):
  """Register XSD template to Django.
    Args:
        xsd_filename:
        xsd_data:
     
    Returns:
  """
  try:
     template = Template(filename=xsd_filename, content=xsd_data)
     template_version_manager = TemplateVersionManager(title=xsd_filename)
     template_version_manager_api.insert(template_version_manager, template)
     logger.info("XSD template:" + xsd_filename + " registered as a template.")
  except exceptions.CoreError as e:
     logger.info(xsd_filename + " didn't registered as a template :" + str(e))
  except exceptions.NotUniqueError as e:
     logger.info(xsd_filename + " didn't registered as a template :" + str(e))
  except Exception as e:
     logger.info(xsd_filename + " didn't registered as a template :" + str(e))


def _set_xsd_type(xsd_filename, xsd_data):
  """Register XSD type to Django.
    Args:
        xsd_filename:
        xsd_data:

    Returns:
  """
  try:
     type_object = Type(filename=xsd_filename, content=xsd_data)
     type_version_manager = TypeVersionManager(title=xsd_filename)
     type_version_manager_api.insert(type_version_manager, type_object)
     logger.info("XSD type:" + xsd_filename + " registered as as type.")
  except exceptions.CoreError as e:
     logger.info(xsd_filename + " didn't registered as a type :" + str(e))   
  except exceptions.NotUniqueError as e:
     logger.info(xsd_filename + " didn't registered as a type :" + str(e))
  except Exception as e:
     logger.info(xsd_filename + " didn't registered as a type :" + str(e))

if __name__ == '__main__':
  path = '/srv/mgi-mdcs/modular-data-models-include/'
  filelist = glob.glob(os.path.join(path, '*.xsd'))

  for filepath in filelist:
     # Get XSD from file
     xsd_filename = os.path.basename(filepath)
     file = open(filepath, 'r')
     xsd_data  = file.read()
        
     # XSD to flat
     flat_xsd = XSDFlattenerFile(xsd_data).get_flat()
     flat_xsd

     # To well-formed XSD
     dom = xml.dom.minidom.parseString(flat_xsd)
     pretty_xml = dom.toprettyxml()

     # Data registration to MDCS  
     _set_xsd_type(xsd_filename, pretty_xml)  
     _set_xsd_template(xsd_filename, pretty_xml)
