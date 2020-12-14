
import unittest
import configparser

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from time import sleep

class Test(unittest.TestCase):

    def setUp(self):
        print('Do something before test')
        self.config = configparser.ConfigParser()
        self.config.read('testConfig.ini')

        #webdriverLocation = ''
        self.browser = webdriver.Chrome(executable_path=self.config['Location']['webdriver'])

    def test_search(self):
        print('testing...')
        self.browser.get('https://www.google.com')
        self.browser.maximize_window()

        searchColumn = self.browser.find_element_by_name('q')
        searchColumn.send_keys('one piece')
        searchColumn.submit()
        #searchBtn = self.browser.find_element_by_name('btnK')
        #searchBtn.send_keys(Keys.RETURN)

    def tearDown(self):
        print('Do something after test')
        sleep(3)
        #self.browser.close()

if __name__ == '__main__':
    unittest.main()    
