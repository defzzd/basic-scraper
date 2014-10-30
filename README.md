basic-scraper
=============


A basic web scraper, using BeautifulSoup4.

No external callables if run as the main program;
    it will print information from craigslist concerning apartments in Seattle.

If imported, return_apartment_search_results() can be called with a
    a minimum of one of the following keyword parameters, formatted as follows:
        return_apartment_search_results(query="Queen Anne",
                                        minAsk=600,
                                        maxAsk=1500,
                                        bedrooms=1)

    The result of calling this function is a pair of variables,
        content and encoding.

    The contents of content may be passed to parse_source(), which will return
        a BeautifulSoup parse.

    This BeautifulSoup parse may then be handed to extract_listings(),
        which will return a generator yielding apartment listings,
        one per apartment.

    These apartment listings may have the CodeFellows address added to them
        when add_address() is called upon them, one at a time.

The main progrm can also be called with the CLI argument test, which will
    run the main cycle of this program without pinging any servers by using
    cached content from the files "search_results.html"
    and "geocode_cache.html", both of which were created by hand using
    write_args_to_a_file(), which takes a filename string and a data string and
    returns the filename after writing it.


Collaborators:
    Charlie Rode
    Jason Brokaw (mostly via github studying)

Resources used:

    https://github.com/jbbrokaw/basic-scraper
    http://codefellows.github.io/python-dev-accelerator/assignments/day11/scraper.html
