import rdflib
from rdflib import Graph
graph = Graph(store='SQLite', identifier="testsql")

# firt time create the store:
graph.open('test.ts')
graph.parse('http://bigasterisk.com/foaf.rdf')
graph.commit()
graph.close()


del graph
reloaded_graph = rdflib.Graph(store="SQLite", identifier='testsql')
reloaded_graph.open('test.ts', create=False)

for s,p,o in reloaded_graph:
    print((s,p,o))