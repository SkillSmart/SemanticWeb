from rdflib import ConjunctiveGraph
from drflib.namespace import FOAF, SKOS, SIOC

#  -- get and parse FOAF RDF File
foaf_graph = ConjunctiveGraph()
foaf_graph.parse('')

# -- get and parse the SKOS RDF File
skos_graph = ConjunctiveGraph()
skos_graph.parse(skos_graph_path)

from rdflib import Namespace
from rdflib.namespace import RDF

# Create Namespaces to bind
sioc_ns = Namespace('http://rdfs.org/sioc/ns#')
dcterms_ns = Namespace('http://purl.org/dc/terms#')

#  create the BlogPost RDF Graph
sioc_gaph = ConjunctiveGraph()

# bind namespaces to the new blogpost graph
sioc_graph.bind('rdf', RDF)
sioc_graph.bind('sioc', sioc_ns)
sioc_graph.bind(dcterms', dcterms_ns')

sioc_graph.parse(sioc_graph_filepath)


# 1. Build the social graph

# get nicknames by ID
nicknames = {}
for id, nick in rdf_graph.query('''
    SELECT ?a ?nick
    WHERE {
        ?a foaf:nick ?nick . },
        initNs={'foaf':FOAF, 'rdfs':RDFS}'''):
        nicknames[str(id)] = str(nick)

# 2. Build a NetworkX graph of the relationships
import networkx as nx
nx_graph = nx.Graph()
for a,b in rdf_graph.query('SELECT ?a ?b' +\
                            'WHERE { ?a foaf:knows ?b . }',
                            initNs={'foaf':FOAF, 'rdfs':RDFS}):
    nx_graph.add_edge(str(a), str(b))


# 3. Identify the Cliques in the Graph
for clique in nx.find_cliques(nx_graph):
    if len(clique)>2:
        print([nicknames[id] for id in clique])

# Calculate the centrality of every node
cent = nx.betweenness_centrality(nx_graph)

# Rank the most central people (the influencers)
most_connected = sorted([(score,id) for id,score in cent.items()], reverse=True)




### Extending the Network of Friends using Linked Data
rdf_graph_query = ('''SELECT ?commonFriend
                      WHERE
                      {
                          ?mr foaf:name "Tim Berners-Lee".
                          ?mb foaf:name "John Cage".
                          ?mr foaf:knows+ ?mv.
                          ?commonFriend foaf:knows ?mv.
                          ?commonFriend foaf:knows ?mr.
                      }''', initNs={'foaf':FOAF})


from rdflib.plugins.sparql import prepareQuery
q = prepareQuery('''SELECT DISTINCT ?author
                    WHERE
                    {
                        ?post sioc:has_creator ?user.
                        ?user foaf:name ?target_user.
                        ?post sioc:topic ?topic.
                        ?topic skos:concept ?concept.

                        {?concept skos:narrower ?taxonomyConcept}
                                    UNION
                        {?concept skos:broader ?taxonomyConcept}.

                        ?blogPost sioc:has_creator ?author.
                        ?blotPost sioc:topic ?postTopic
                        ?postTopic skos:concept ?taxonomyConcept.

                        FILTER (?user != ?author &&
                                NOT EXISTS{?user foaf:knows ?author})
                                }''', initNs={'foaf':FOAF, 'skos':SKOS, 'sioc':SIOC})

# Now we can use the query with a dict Binding to retrieve the relevant results from the graph
rdf_graph.query(q, initBindings={'target_user': tim_lee})