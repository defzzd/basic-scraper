'''
Our goal is to write a Python function that will return the search results
HTML from a query to craigslist. This function should:

    It will accept one keyword argument for each of the possible query values

        in tutorial:
        keywords: query=keyword+values+here
        price: minAsk=NNN maxAsk=NNN
        bedrooms: bedrooms=N (N in range 1-8)

        on cl:
        type="text" placeholder="search apts/housing for rent" name="query" id="query" value="" autocorrect="off" autocapitalize="off" autocomplete="off" data-suggest="search" class="flatinput ui-autocomplete-input">

    It will build a dictionary of request query parameters
        from incoming keywords



    It will make a request to the craigslist server using this query
    It will return the body of the response if there is no error
    It will raise an error if there is a problem with the response
'''

import requests
from bs4 import BeautifulSoup
import json  # Used for Google's Geocode API
import pprint  # "Pretty Printing," I think. From tutorial suggestions at:
# http://codefellows.github.io/python-dev-accelerator/
#    assignments/day11/scraper.html

import sys  # To add testing flag for execution block


# Maintaining the name of the search parameters
# for consistency with the website
def return_apartment_search_results(query=None,
                                    minAsk=None,
                                    maxAsk=None,
                                    bedrooms=None):

    # Check bedroom count validity before building the dictionary
    if bedrooms is not None and ((bedrooms > 8) or (bedrooms < 1)):
        raise ValueError("bedrooms must be between 1 and 8, or omitted.")

    # Construct a dictionary for the requests library to use:
    dictionary_of_search_arguments = dict()
    if query is not None:
        dictionary_of_search_arguments['query'] = query
    if minAsk is not None:
        dictionary_of_search_arguments['minAsk'] = minAsk
    if maxAsk is not None:
        dictionary_of_search_arguments['maxAsk'] = maxAsk
    if bedrooms is not None:
        dictionary_of_search_arguments['bedrooms'] = bedrooms

    if len(dictionary_of_search_arguments) == 0:
        raise ValueError("You must enter keywords to search for an apartment.")

    apartment_search_url = 'http://seattle.craigslist.org/search/apa'

    # Using requests library:
    response = requests.get(apartment_search_url,
                            params=dictionary_of_search_arguments,
                            timeout=3)

    # Requests library's functionality for raising an error if it's not 200 OK
    response.raise_for_status()

    return response.content, response.encoding


def parse_source(content, encoding='utf-8'):

    beautiful_parse = BeautifulSoup(content, from_encoding=encoding)

    return beautiful_parse


def return_data_from_file(file_name):

    with open(file_name, 'r') as the_file:
        return the_file.read()


def write_args_to_a_file(file_name, what_to_write):

    # Use this to keep from over-requesting
    # the server you're pinging while testing.

    # This function needs to raise an exception.
    with open(file_name, 'w') as the_file:
        the_file.write(str(what_to_write))

    return file_name


def extract_listings(parsed_html):
    ''' Further parsing of BeautifulSoup '''
    apartment_listings = parsed_html.find_all('p', class_='row')
    extracted = []
    for each_listing in apartment_listings:
        location = {'data-latitude': u'47.6235481', 'data-longitude': u'-122.336212',}
        link = each_listing.find('span', class_='pl').find('a')
        price_span = each_listing.find('span', class_='price')
        compiled_listing = {
            'location': location,
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price_span.string.strip(),
            'size': price_span.next_sibling.strip(' \n-/')
        }
        # The tutorial says generators have a lower memory footprint.
        # I'd never thought about it before, but suddenly this makes me
        # want to generatorize all the lists...!
        yield compiled_listing


def get_addresses(apartment_listing):

    # The universal resource locator where Google's
    # Geocode application programming interface lives.
    url_for_the_api = 'http://maps.googleapis.com/maps/api/geocode/json'
    # Hardcoded to Code Fellows, since craigslist changed how they work.
    loc = apartment_listing['location']
    # Next is a format string, used by the string formatting call below it.
    latlng_tmpl = "{data-latitude},{data-longitude}"
    parameters = {
        'sensor': 'false',
        'latlng': latlng_tmpl.format(**loc),
    }
    # Actually pinging Google. This line sends a real-world HTTP request!
    response = requests.get(url_for_the_api, params=parameters)
    return response

def add_address(apartment_listing, testing=False):
    if testing == True:
        apartment_listing = return_data_from_file("geocode_cache.html")
    else:
        response = get_addresses(apartment_listing)
        # Check the HTTP error code for a problem and raise an exception if so:
        response.raise_for_status()
        data_from_google = json.loads(response.text)
        if data_from_google['status'] == 'OK':
            # This selects the first address Google returns for a given latlng:
            first_result = data_from_google['results'][0]
            apartment_listing['address'] = first_result['formatted_address']
        else:
            apartment_listing['address'] = 'unavailable'
    return apartment_listing


if __name__ == "__main__":

    # Testing with html saved in a file on my drive:
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        content = return_data_from_file("search_results.html")
        encoding = 'utf-8'  # Works
        testing = True
        parsed_html = parse_source(content, encoding)
        for each_apartment_listing in extract_listings(parsed_html):
            # Adding Geocode data... for CodeFellows:
            listing_with_address = add_address(each_apartment_listing, testing=testing)
            pprint.pprint(listing_with_address)
            break

    else:
        content, encoding = return_apartment_search_results(query="Queen Anne",
                                    minAsk=600,
                                    maxAsk=1500,
                                    bedrooms=1)
        testing = False

        parsed_html = parse_source(content, encoding)
        for each_apartment_listing in extract_listings(parsed_html):
            # Adding Geocode data... for CodeFellows:
            listing_with_address = add_address(each_apartment_listing, testing=testing)
            pprint.pprint(listing_with_address)
