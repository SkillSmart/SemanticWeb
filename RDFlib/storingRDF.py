# Persistence
from rdflib import Literal
import rdflib

store = rdflib.plugin.get("SQLite", rdflib.store.Store)('rdf-test.ts')
store.open('home', create=False)

g = rdflib.ConjunctiveGraph(store)

dbpedia_res = rdflib.Namespace("<http://www.dbpedia.org/resource/")
dbpedia = rdflib.Namespace("<http://www.dbpedia.org/ontology/")

g.add((dbpedia_res["Python_(programming_language)"],
    dbpedia["influenced"],
    Literal("Cobra Language")))

g.serialize(format='nt')
g.commit()