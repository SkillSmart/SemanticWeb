# # import rdflib

# # g = rdflib.Graph()
# # result = g.parse("http://www.w3.org/People/Berners-Lee/card")
# # for s, p, o in g:
# #     if (s,p,o) not in g:
# #         raise Exception("It better be!")

# # s = g.serialize(format="n3")


# # Generating a person node and adding attributes from different Namespaces to it
# from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
# from rdflib.namespace import DC, FOAF

# g = Graph()

# donna = BNode()

# g.add( (donna, RDF.type, FOAF.Person) )
# g.add( (donna, FOAF.nick, Literal("donna", lang='en')) )
# g.add( (donna, FOAF.name, Literal("Donna False")) )
# g.add( (donna, FOAF.mbox, URIRef("mailto:donna@example.com")) )

# # Printing out the tripples associated with the Graph
# for s,p,o in g:
#     print((s,p,o))

# # Printing the Mailbox for all subjects in the TS
# for person in g.subjects(RDF.type, FOAF.Person):
#     for mbox in g.objects(person, FOAF.mbox):
#         print(mbox)

# #  Bind a few prefix, namespace pairs for more readable output
# g.bind("dc", DC)
# g.bind("foaf", FOAF)

# print( g.serialize(format="n3"))


# # Loading and saving Tripples
# print("\n\n Loading and Saving Tripples")

# from rdflib import Graph

# g = Graph()
# g.parse("RDFlib/demo.nt", format="nt")
# print(len(g))

# import pprint
# for stmt in g:
#     pprint.pprint(stmt)


# # Reading in remote Graphs
# print("\n\n Loading in remote Graphs")

# g.parse("http://bigasterisk.com/foaf.rdf")
# print('The loaded FOAF file contains %i assertiions' % len(g))


# # Creating RDF Tripplets


# # 1. Creating Nodes
# from rdflib import URIRef, BNode, Literal

# # bob = URIRef("http://example.org/people/Bob")
# # linda = BNode()

# # name = Literal('Bob')
# # age = Literal(24)
# # height = Literal(76.5)


# # # Creating multiple Attributes within a given namespace
# # n = Namespace("http://example.org/people/")

# # n.bob
# # n.eve


# # # Using most common namespaces within rdflib
# # print('\n\n Using built in namespaces')
# # from rdflib.namespace import RDF, FOAF
# # print(RDF.type)
# # print(FOAF.knows)

# # # Adding Triples

# # g = Graph()

# # g.add( (bob, RDF.type, FOAF.Person))
# # g.add( (bob, FOAF.name, name) )
# # g.add( (bob, FOAF.knows, linda) )
# # g.add( (linda, RDF.type, FOAF.Person) )
# # g.add( (linda, FOAF.name, Literal('Linda')) )

# # print(g.serialize(format="turtle"))

# # # Removing Triples
# # g.remove( (bob, None, None) ) # Removes Bob from the Graph


# Adding nodes based on usage
# import rdflib
# from rdflib.namespace import FOAF

# f = rdflib.Graph()
# f.parse("http://danbri.livejournal.com/data/foaf/")
# for s, _, n in f.triples((None, FOAF['member_name'], None)):
#     f.add((s, FOAF['name'], n))


# Navigating Graphs
# for s,p,o in graph:
#     if not (s,p,o) in graph:
#         raise Exception("Iterator/Container Protocols are broken!")


# Check a graph on combinations of Triplet information
'''
from rdflib import URIRef
from rdflib.namespace import RDF

bob = URIRef("http://example.org/people/bob")
if ( bob, RDF.type, FOAF.Person ) in graph:
    print("This graph knows that Bob is a person")

if (bob, None, None) in graph:
    print("This graph contains information about Bob")


# Set operations on RDFLib Graphs
g1 = Graph()
g2 = Graph()

# Union
g1 + g2
g1 =+ g2

# Difference
g1 - g2
g1 -= g2

# Intersection
g1 & g2
# xor
g1 ^ g2
'''

# Basic Triple Matching using the triples() function
'''
g.load("some_foaf.rdf")
for s,p,o in g.triples((None, RDF.type, FOAF.Person)):
    print('%s is a s %s'%(s,o))

# Extracting a subset of nodes
bobgraph = g.triples((bob, None, None))
'''

# Extracting triplet parts
'''
g.subjects(RDF.type, FOAF.Person)
name = g.value(bob, FOAF.name) # Get any name for Bob
mbox = g.value(predicate = FOAF.name, object = bob, any = False) # Retrieve a single object for a subject, and raise Exception if more are found

# Convenience Functions on graphs
g.triples()
g.value(None, FOAF.knows, Linda) #Returns the Value for all subjects knowing Linda
g.subjects()
g.preferredLabel

'''

from rdflib import ConjunctiveGraph, URIRef, RDFS, Literal
from rdflib.namespace import SKOS
from pprint import pprint

g = ConjunctiveGraph()
u = URIRef(u'http://example.com/foo')
g.add([u, RDFS.label, Literal('foo')])
g.add([u, RDFS.label, Literal('bar')])

pprint(sorted(g.preferredLabel(u)))

g.add([u, SKOS.prefLabel, Literal('bla')])
print (g.preferredLabel(u))
g.add([u, SKOS.prefLabel, Literal('blubb', lang='en')])


# 