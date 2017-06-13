from rdflib import Graph

g = Graph()
g.parse("RDFlib/demo.nt", format="nt")

# print the resulting graph length
print(len(g))

import pprint
for stmt in g:
    pprint.pprint(stmt)



# Reading a remote Graph
g.parse("http://bigasterisk.com/foaf.rdf")
for stmt in g:
    pprint.pprint(stmt)