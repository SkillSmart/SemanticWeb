from rdflib import URIRef, BNode, Literal

bob = URIRef("http://example.org/people/Bob")
linda = BNode() # a GUID is generated

# Nodes can be created by the construction of node classes:
name = Literal("Bob")
age = Literal(24)
height = Literal(76.5)

# For creating multiple URIRefs in the sname namespace we use
from rdflib import Namespace

n = Namespace("http://example.org/people/")

n.bob
n.eve

# RDFlib predefines Namespaces for the most commonly used Ontologies
from rdflib.namespace import RDF, FOAF

print(RDF.type)
print(FOAF.knows)
