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
        parsed_html = scraper.extract_listings(self.parsed_html)
        testing_dictionary = parsed_html[0]
        assert isinstance(testing_dictionary, dict)
        assert isinstance(testing_dictionary['size'], unicode)
        assert "br" in testing_dictionary['size']
        assert isinstance(testing_dictionary['description'], unicode)
        assert isinstance(testing_dictionary['link'], unicode)
        assert "html" in testing_dictionary['link']
        assert isinstance(testing_dictionary['price'], unicode)
        assert '$' in testing_dictionary['price']
        assert testing_dictionary['price'].strip("$").isdigit()


unittest.main()


'''

    class pj
    --12--
    --13--
    --15--
    --16--
    --17--
    --18--
          19

'''