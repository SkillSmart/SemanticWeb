import rdflib
from rdflib import URIRef
from rdflib.graph import ConjunctiveGraph
import pprint

g = ConjunctiveGraph()

g.parse("http://live.dbpedia.org/data/Python_(programming_language).ntriples", format='nt')

# for triple in g:
#     print(triple)

print(list( g.triples((None, rdflib.URIRef('rdf:about'), None)) ))

g.add(URIRef("<http://dbpedia.org/resource/Python_(programming_language)>"),
      URIRef("http://dbpedia.org/ontology/influenced"),
      URIRef("http://dbpedia.org/resource/Cobra_(programming_language)")
)

# Save the Graph to an output file
outfile = open("colin.xml", "w")
outfile.write(g.serialize(format="pretty-xml"))