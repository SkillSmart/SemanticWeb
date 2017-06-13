import rdflib
from rdflib import Graph

graph = Graph('SQLite', 'testsql')
graph.open('test.ts', create=False)

print(len(graph))