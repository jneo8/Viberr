from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from pyvirtualdisplay import Display

class NewVisitorTest(unittest.TestCase):

    # browser = webdriver.Safari()

    def setUp(self):
        display = Display(visible=0, size=(800, 800))  
        display.start()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8090/superlist')

      
if __name__ == '__main__':
    unittest.main(warnings='ignore')