import unittest
from tests import BaseTestCase
from selenium import webdriver


class PagesLoadingCorrectly(BaseTestCase):
    """
    Functional tests for loading pages
    """

    # def test_index_page_loads_correctly(self):
    #     # self.browser = webdriver.Chrome("/usr/bin/chromedriver")
    #     # self.browser.quit()
    #
    #     self.browser.get('http://localhost:5000')
    #     self.assertIn("Hadithi", self.browser.title)

    # def test_categoty_page_populates_database(self):
    #     """Category page updates database successfully"""
    #     self.browser.get('http://localhost:5000/application')
    #
    #     # find all form input fields via form name
    #     _inputs = self.browser.find_elements_by_xpath('//form[@name="signup-form"]//input')
    #
    #     for input in _inputs:
    #         # print attribute name of each input element
    #         print(id.get_attribute('name'))
    #
    #     self.assertIn("Hadithi", self.browser.title)


if __name__ == '__main__':
    unittest.main()
