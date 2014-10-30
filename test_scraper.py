import unittest
import scraper

# This test file was greatly helped by my reading Jason Brokaw's tests at:
# https://github.com/jbbrokaw/basic-scraper/blob/master/test_scraper.py




class test_Scraper(unittest.TestCase):

    def setUp(self):


        # I actually went with Queen Anne at first as well
        # because it was a memorably-named part of town,
        # and it was likely to have 1-bedrooms in the
        # (wide) range I used as default values.
        self.content, self.encoding = scraper.return_apartment_search_results(
            query="Queen Anne")

        self.parsed_html = scraper.parse_source(self.content, self.encoding)

        # Some tests also run when setting up...
        # Should be just like an actual query:
        assert self.encoding == 'utf-8'
        assert "Queen Anne" in self.content

    def test_return_apartment_search_results(self):


        with self.assertRaises(ValueError):
            scraper.return_apartment_search_results()
        with self.assertRaises(ValueError):
            scraper.return_apartment_search_results(bedrooms=15246)
        with self.assertRaises(ValueError):
            scraper.return_apartment_search_results(bedrooms=-4)
        with self.assertRaises(ValueError):
            scraper.return_apartment_search_results(bedrooms='qwerty')
        with self.assertRaises(ValueError):
            scraper.return_apartment_search_results(bedrooms='')
        with self.assertRaises(ValueError):
            scraper.return_apartment_search_results(bedrooms=None)

    def test_parse_source(self):

        with self.assertRaises(TypeError):
            # Needs args to work.
            scraper.parse_source()

        with self.assertRaises(TypeError):
            # Needs _particular kinds_ of args to work!
            scraper.parse_source(None)


    def test_extract_listings(self):

        with self.assertRaises(TypeError):
            # Needs args to work.
            scraper.extract_listings()



        # This particular block was copy-pasted and edited to match my code...
        # https://github.com/jbbrokaw/basic-scraper/blob/master/test_scraper.py
        # ... after I understood what it did.
        parsed_html = scraper.extract_listings(self.parsed_html).next()
        testing_dictionary = parsed_html
        assert isinstance(testing_dictionary, dict)
        assert isinstance(testing_dictionary['size'], unicode)
        assert "br" in testing_dictionary['size']
        assert isinstance(testing_dictionary['description'], unicode)
        assert isinstance(testing_dictionary['link'], unicode)
        assert "html" in testing_dictionary['link']
        assert isinstance(testing_dictionary['price'], unicode)
        assert '$' in testing_dictionary['price']
        assert testing_dictionary['price'].strip("$").isdigit()


    def test_add_address(self):

        # This test function inspired by and partially paraphrased from:
        # https://github.com/jbbrokaw/basic-scraper/blob/master/test_scraper.py

        # Also tests extract_listings(), parse_source()
        # and return_data_from_file().

        with self.assertRaises(TypeError):
            scraper.add_address()
        with self.assertRaises(TypeError):
            scraper.add_address(None)

        content = scraper.return_data_from_file('search_results.html')
        encoding = 'utf-8'
        parsed_html = scraper.parse_source(content, encoding)
        apartment_listing = scraper.extract_listings(parsed_html).next()

        assert 'data-latitude' in apartment_listing['location']
        assert 'data-longitude' in apartment_listing['location']





unittest.main()
