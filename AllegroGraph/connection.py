import tempfile

from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.miniclient import repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.model import URI
from franz.openrdf.vocabulary.rdf import RDF
from franz.openrdf.vocabulary.rdfs import RDFS
from franz.openrdf.vocabulary.owl import OWL
from franz.openrdf.vocabulary.xmlschema import XMLSchema
from franz.openrdf.query.dataset import Dataset
from franz.openrdf.rio.rdfformat import RDFFormat
from franz.openrdf.rio.rdfwriter import  NTriplesWriter
from franz.openrdf.rio.rdfxmlwriter import RDFXMLWriter

import os, urllib, datetime, time, sys

CURRENT_DIRECTORY = os.getcwd()

# Directory containing the data files.
# Use the location of the script file or the current working
# directory if that location is not known.
BASE_DIR = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()

AG_HOST = os.environ.get('AGRAPH_HOST', 'localhost')
AG_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AG_CATALOG = os.environ.get('AGRAPH_CATALOG', '')
# Every example uses this repository except example16(),
# which creates 2 repos: redthings and greenthings, 
AG_REPOSITORY = 'pythontutorial'
AG_USER = os.environ.get('AGRAPH_USER', 'test')
AG_PASSWORD = os.environ.get('AGRAPH_PASSWORD', 'xyzzy')

RAISE_EXCEPTION_ON_VERIFY_FAILURE = False

# Connect to a local AllegroGraph Server

server = AllegroGraphServer(AG_HOST, AG_PORT, AG_USER, AG_PASSWORD)
print ("Available catalogs", server.listCatalogs())