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












def return_from_search_results_file(file_name):

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
        extracted.append(compiled_listing)
    return extracted



if __name__ == "__main__":

    # Testing with html saved in a file on my drive:
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        content = return_from_search_results_file("search_results.html")
        encoding = 'utf-8'  # Works
    else:
        content, encoding = return_apartment_search_results(query="Queen Anne",
                                    minAsk=600,
                                    maxAsk=1500,
                                    bedrooms=1)

    parsed_html = parse_source(content, encoding)
    apartment_listings = extract_listings(parsed_html)
    print(len(apartment_listings))
    pprint.pprint(apartment_listings[0])  # Suggested by tutorial; see imports
