from rdflib.graph import ConjunctiveGraph
from rdflib import namespace
from rdflib import Namespace, BNode, Literal, RDF, URIRef
import csv
import simplejson
import requests
import sys


"""
This module contains of all relevant methods to import and parse 
Job Posting Data into the Ontology.

- Parsing Methods are applied to automatically turn Crawler Exports into RDF
- Import Formats are kept in csv for simplicity
"""

# General Convenience Functions for the Module

class JoblistParser:
    """
    Accepts a graph onto which to annotate the new information and 
    a filelocation from which to retrieve the information in CSV Format.
    """
    def __init__(self, graph, filename):
        """
        Instantiates the csv filename and the graph onto which to 
        append the extracted information.
        """
        self.file = open(filename, 'r+')
        self.graph = graph

    def parse_csv(self):
        """
        Parses RDF Data from a given CSV File containing information about open positions
        from the Spider Module.

        !For now, the schema is hardcoded here. This should be developed to be changed into 
        a OWL Schema to be picked up later to enable fast changes in data layout
        """
        return csv.reader(self.file)
    
    def parse_json(self, jsonobject):
        """
        Parses RDF Data from a given JSON File
        """
        return simplejson.loads(jsonobject)

    
    def create_graph(self):
        """
        Takes the information from the file and reads them into a joblist graph.
        """
        # Create the Namespaces to describe Job and Company related information
        SCHEMA = Namespace("https://schema.org/")
        JOBS = Namespace("https://schema.org/JobPosting")
        ORG = Namespace("https://schema.org/Organization")
        CORP = Namespace("https://schema.org/Corporation")
        RDFS = namespace.RDFS
        RDF = namespace.RDF
        JB = Namespace("http://smartrecruiting.com/schemas/jobboard#")

        # Append the API Adresses used for the services
        crunchbase_api = "http://api.crunchbase/com/v/1/company/%s.js"

        # Create the Graph and Attach the Namespace bindings for abstraction
        jg = ConjunctiveGraph()
        jg.bind('jobs', JOBS)
        jg.bind('org', ORG)
        jg.bind('corp', CORP)
        jg.bind('rdfs', RDFS)
        jg.bind('rdf', RDF)
        jg.bind('schema', SCHEMA)

        vid = 0
        # Create the Graph
        for title, salary, location, company, crunchbase, ticker in self.parse_csv():
            # Create the vacancy
            vid += 1
            vacancy = JB[str(vid)]
            jg.add((vacancy, RDF.type, SCHEMA['JobPosting']))
            jg.add((vacancy, JOBS['title'], Literal(title)))

            # Add the location to the data
            location_id = location.lower().replace(' ', '_').replace(',', '')
            # jg.add((vacancy, JOBS['joblocation'], JB[location _id]))
            jg.add((vacancy, JOBS['salaryCurrency'], Literal('USD')))
            jg.add((vacancy, JOBS['baseSalary'], Literal(salary)))

            # Create the company Nodes and append attributed information
            cnode = JB[company.lower().replace(' ', '_')]
            jg.add((cnode, RDF.type, SCHEMA['Organization']))
            jg.add((cnode, ORG['legalName'], Literal(company)))
            jg.add((vacancy, JOBS['hiringOrganization'], cnode ))
            
            # Ticker Symbol
            if ticker != "":
                jg.add((cnode, CORP['tickerSymbol'], Literal(ticker)))
            # Crunchbase Link
            if crunchbase != "":
                jg.add((cnode, RDFS['seeAlso'], Literal(crunchbase_api % crunchbase)))
        
        # Return the Graph 
        graph.update(jg)

    
    def update_crunchbase(self):
        """
        Update the existing Graph within Crunchbase information for all available
        'seeAlso' links.
        """

        
        # Check the graph
        print(jg.serialize(format="n3"))

graph = ConjunctiveGraph(store="SQLite")
graph.open('test.ts', create=False)

jobs = JoblistParser(graph, './data/joblist.csv').parse_csv() 
for row in jobs:
    print(row)


JoblistParser(graph, './data/joblist.csv').create_graph()
