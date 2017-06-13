"""
This module contains all methods necessary to connect to and retrieve information from 
"""
# Imports for Graph Creation and management
from rdflib import ConjunctiveGraph, BNode, Literal, Namespace
from rdflib.namespace import FOAF, RDFS

import pycrunchbase
import simplejson
import requests

from urllib.parse import quote_plus
from settings import settings

class CrunchbaseAPI(object):
    """
    define all necessary interactions with the Crunchbase API to work within our
    system. This class entails wrapper functions for common interactions and 
    also integrates the scraping functionalities to retrieve additional content from
    the page as needed.
    """

    def __init__(self):
        pass
    
    def _get_query(self, queryType, search_type, search_string, **filters):
        """
        Accepts: A queryDict that entails the list of all accepted query Parameters for the
        OpenCompany API
        Given the keyword arguments, this function creates a querystring for the API
        Settings:
        - Set to search either organizations or people
        """
        # Create the basic API HTTP Request string
        query_request = {
            'org_list': settings.CRUNCHBASE_API_URL + "odm-organizations" +"{}"+ "&?user_key="+settings.CRUNCHBASE_API_KEY,
            'person_list': settings.CRUNCHBASE_API_URL + "odm-people" +"{}"+ "&user_key="+settings.CRUNCHBASE_API_KEY,
            'org': settings.CRUNCHBASE_API_URL + "odm-organizations" +"{}"+ "&user_key="+settings.CRUNCHBASE_API_KEY,
            'person': settings.CRUNCHBASE_API_URL + "odm-people" +"{}"+ "&user_key="+settings.CRUNCHBASE_API_KEY,
            }

        # Free API support searching ()
        '''Provides all accessible query and filtering terms for the API Request on the Crunchbase ODM'''
        search_filter={
            'org_search': {
                'query': '?query=',
                'name': '?name=',
                'domain_name': '?domain_name=',
            },
            'org_filter': {
                'org_types': '&organization_types=',
                'location_uuids': '&location_uuids=',
                'category_uuids': '&category_uuids='
            },
            'person_search': {
                'name':'?name=',
                'query': '?query=',
            },
            'person_filter': {
                'updated_since': '&updated_since=',
                'sort_order': '&sort_order=',
                'locations': '&locations=',
                'socials': '&socials=',
                'types': '&types='
            }
        }
        
        # Select the search filters applicable to a given Type of query
        query = ""
        search_category = queryType.split("_")[0]

        # Add the search string to the query
        if search_string:
            query += search_filter[search_category+"_search"][search_type]+quote_plus(search_string)
        
        # For each filter argument add the filter string to the query
        # Expects the Filters to be passed as keyword arguments
        if filters:
            for parameter, filter_string in filters.items():
                query += search_filter[search_category+"_filter"][parameter]+quote_plus(filter_string)

        # Put it all together
        return query_request[queryType].format(query)

    def _queryApi(self, query):
        try:
            return requests.get(query)
        except:
            raise Exception("Crunchbase API Connection failed")

    def updateCompany(self, companyName, **filters):
        """
        Annotate Information about a Company 
        """
        # Retrieve the Company Data from the Crunchbase API
        request =  self._queryApi(self._get_query(queryType="org",search_type="name", search_string=companyName, **filters))

        # Append resulting Information to a new graph
        CRUNCHBASE = Namespace('http://www.openlinksw.com/schemas/crunchbase#')
        # Create a graph and append the nodes
        cg = ConjunctiveGraph()
        cg.bind('cb', CRUNCHBASE)
        company = BNode()
        # Extract the information from the Response
        for k,v in request.json()['data']['items'][0]['properties'].items():
            cg.add((company, CRUNCHBASE[k], Literal(v)))
        
        # Serialize the Data for Testing
        return cg.serialize(format='n3')

    def updatePerson(self, search_string, search_type="name", **filters):
        """
        Annotate Information on a given Person
        """
        # Retrieve the Company Data from the Crunchbase API
        request =  self._queryApi(self._get_query(queryType="person",search_type="name", search_string=search_string, **filters))

        # Append resulting Information to a new graph
        CRUNCHBASE = Namespace('http://www.openlinksw.com/schemas/crunchbase#')
        PERSON = Namespace("http://schema.org/Person#")
        # Create a graph and append the nodes
        cg = ConjunctiveGraph()
        cg.bind('cb', CRUNCHBASE)
        cg.bind('person', PERSON)

        # Create the Person Node according to the Overall SmartRecruiting Graph
        person = BNode()

        # This creates a mapping between the Crunchbase and the 

        # Map the information from the Crunchbase to Schema.org Ontology
        cb_foaf_mapping = {
            'first_name': 'givenName',
            'last_name': 'familiyName',
            'gender': 'gender',
            'city_name': 'homeLocation',
            'title': 'jobTitle',
            'organization_permalink': 'memberOf',

        }
        for k,v in request.json()['data']['items'][0]['properties'].items():
            # Check if Person related information (map to FOAF)
            if k in cb_foaf_mapping:
                cg.add((person, FOAF[cb_foaf_mapping[k]], Literal(v)))
            # Else map it to the Crunchbase Ontology
            else:
                cg.add((person, CRUNCHBASE[k], Literal(v)))
        # Serialize the Data for Testing
        return cg.serialize(format='n3')

class OpenRefine(object):
    """
    The wrapper class to enhance Corporate Data trough the "Open Corporates" Database API. 
    """

    def __init__(self):
        self.api_baseurl = settings.OPENCORPORATES_API_URL
        
    
    def _get_query(self, queryDict):
        """
        Accepts: A queryDict that entails the list of all accepted query Parameters for the
        OpenCompany API
        Given the keyword arguments, this function creates a querystring for the API"""

         # Create the Searchstring based on the passed information
        query = self.api_baseurl
        if queryDict['name'] != "":
            query += "q={}".format(queryDict['name'])
        if queryDict['id'] != "":
            query += "&"
        if queryDict['industry_codes'] != "":
            query += "&industry_codes={0}".format(queryDict['industry_codes'])
        if queryDict['country_code'] != "":
            query += "&country_code={0}".format(queryDict['country_code'])
        if queryDict['jurisdiction_code'] != "":
            query += "&jurisdiction_code={0}".format(queryDict['jurisdiction_code'])
        if queryDict['company_type'] != "":
            query += "&company_type={0}".format(queryDict['company_type'])
        if queryDict['current_status'] != "":
            query += "&current_status={0}".format(queryDict['current_status'])
        if queryDict['registered_address'] != "":
            query += "&registered_address={0}".format(queryDict['registered_address'])
        if queryDict['created_since'] != "":
            query += "&created_since={0}".format(queryDict['created_since'])
        if queryDict['incorporation_date'] != "":
            query += "&incorporation_date={0}".format(queryDict['incorporation_date'])

        return query
    
    def _queryApi(self, query):
        """Executes a query against a given API"""
        try:
            data = simplejson.loads(requests.request(query))
        except: 
            raise Exception('API Request failed to process')

    def match_company(self, companyItem):
        """
        Creates a queryDict from the existing companyItem to match the company against the OpenCompany Database
        """ 
        
        # Retrieve the relevant information from the companyItem
        queryDict = {
            'name': 'xxx',
            'id': 'id',
            'industry_codes': 'xxx',
            'country_code': 'xxx',
            'jurisdiction_code': 'xxx',
            'company_type': 'xxx',
            'registered_address': 'xxx',
            'created_since': 'xxx',
            'incorporation_date': 'xxx',
        }

    def list_companies(self):
        """Extracts a list of matching Companies"""

        # Identify Companies by Jurisdiction

    def annotate_graph(self, graph):
        """
        Identifies comapny relevant information in the graph and tries to annotate the information with 
        OpenCompany LinkedData.
        """

        # Extract a list of all companies from the Graph that do not have specific values

        # Iterate over the list and fetch the results for each Company

        # Transform the Data into RDF and attach the new information onto a in-memory graph

        # Make sure the new graph is consistent with the existing graph

        # Join the new graph and the existing graph





class IndeedAPI(object):
    """
    Defines all interactions with the Indeed Network globally.
    Instances are created for a specific language / Country
    """
    def __init__(self, country):
        """
        Instance can be created for a specific country
        """
        # Adapt the Searchquery based on location and 
        self.country = country

    
    def _get_query(self,**kwargs):
        """
        Creates the Request Header for searching the Indeed Plattform for 
        a specific country.
        """
        # Prepare the content for the http Request
        if kwargs['phrase'] !="":
            kwargs['phrase'] = kwargs['phrase'].replace(' ', '+')
        if kwargs["wordgroup"] !="":
            kwargs["wordgroup"] = kwargs["wordgroup"].replace(' ', '+')
        if kwargs["without"] !="":
            kwargs["without"] = kwargs["without"].replace(' ', '+')
        if kwargs["title"] !="":
            kwargs["title"] = kwargs["title"].replace(' ', '+')

        # Define the Search Term Replacements for each country
        queries = {
            'de' : '''https://de.indeed.com/Jobs?as_and={terms}
                  &as_phr={phrase}
                  &as_any={wordgroup}
                  &as_not={without}
                  &as_ttl={title}
                  &as_cmp={comp}
                  &st={location}
                  &radius={radius}
                  &l={l}
                  &fromage={age}
                  &limit={limit}
                  &sort={sort}
                  &psf=advsrch''',
            'us' : '''https://de.indeed.com/Jobs?as_and={terms}
                  &as_phr={phrase}
                  &as_any={wordgroup}
                  &as_not={without}
                  &as_ttl={title}
                  &as_cmp={comp}
                  &st={location}
                  &radius={radius}
                  &l={l}
                  &fromage={age}
                  &limit={limit}
                  &sort={sort}
                  &psf=advsrch''',
        }

        # return queries[self.country]
        return queries[self.country].format(**kwargs)

    def _crawl_jobs(self, terms="", phrase="", wordgroup="", without="", title="", comp="", 
                   location="", radius=25, salary="", l="", age="any", limit=100, sort=""):
        """
        Translates the search terms into a http request and calls the appropriate
        spider to extract the information from the returned pages.
        """

        # Create the Query based on the Terms
        return self._get_query(terms=terms, phrase=phrase, wordgroup=wordgroup, without=without, title=title,
                                comp=comp, location=location, radius=radius, l=l, salary=salary,
                                age=age, limit=limit, sort=sort)
        
        # Engage the right Spider to do the job


        #  



    def create_jobsearch(self):
        """
        Creates an iterative Jobsearch process given a specific set of criteria

        It

        It implements:
        - Search all available jobs in a country for a given term
            - It will use the job taxonomy to apply synonym search
            - It will use the industry taxonomy to search all jobs in a specific industry
            - It will use th 
        """




# Testrun the Module

# a = IndeedAPI('de')
# print (a.crawl_jobs())

b = CrunchbaseAPI()
# print(b._get_query(queryType='org', search_type="name", search_string="hiq", location_uuids='California,US'))
print(b.updateCompany(companyName='hiq labs'))
# print(b.updatePerson(search_string="Elon Musk"))
