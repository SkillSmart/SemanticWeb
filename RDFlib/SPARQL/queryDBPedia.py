import rdflib
from rdflib.plugins.sparql import prepareQuery

q = prepareQuery('''
    SELECT ?object WHERE
    {?language dbpedia:influenced ?object.}''',
    initNs={'dbpedia':'http://dbpedia.org/ontology/'})

g = rdflib.Graph()
g.parse("http://dbpedia.org/resource/Python_(programming_language)", format="nt")

python = rdflib.URIRef("http://dbpedia.org/resource/Python_(programming_language)")
for row in g.query(q, initBindings={'language': python}):
    print(row)

for row in g:
    print(row)