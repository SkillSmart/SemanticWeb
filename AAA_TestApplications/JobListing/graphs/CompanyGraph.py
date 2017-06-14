"""
Usecases for the graph:
- Store new information on companies we have found on the web
- Use the knowledge in the graph to pinpoint the relevant Schema Term for a new entity
- Use the knowledge in the graph about an identified entity to classifiy new attributes
  with the appropriate Schema Term
- Use a list of predefined logical functions to annotate more information from the given
  Data automatically
- 

Actions to be performed on the graph:




"""
from rdflib.graph import ConjunctiveGraph
from rdflib import BNode, Namespace, Literal, RDF, RDFS, URIRef
import requests


# Define the Core Graph Classes
class BaseGraph(object):
    def __init__(self):
        pass


    


class CompanyGraph(Graph):
    def __init__(self):
        pass


# First check if graph exists and if so load | if not create

# Load the necessary Namespaces

# 



# What to do with the graph


"""