
import unittest
import configparser

from time import sleep

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains

class Test(unittest.TestCase):

    def setUp(self):
        print('Do something before test')
        self.config = configparser.ConfigParser()
        self.config.read('testConfig.ini')

        #webdriverLocation = ''
        self.browser = webdriver.Chrome(executable_path=self.config['Location']['webdriver'])

    def tearDown(self):
        print('Do something after test')
        sleep(3)
        #self.browser.close()

    def newWeb(self, web='', url=''):
        if web:
            self.browser.get(self.config['Web']['web_{}'.format(web)])
        elif url:    
            self.browser.get(url)

        sleep(2)    

    def newTable(self, table='', url=''):
        self.browser.execute_script('window.open()')
        self.browser.switch_to_window(self.browser.window_handles[-1])

        if table:
            self.browser.get(self.config['Web']['web_{}'.format(table)])
        elif url:    
            self.browser.get(url)

        sleep(2)

    def closeTable(self):
        print('@@1 window handles:', self.browser.window_handles)
        self.browser.close()
        print('@@2 window handles:', self.browser.window_handles)
        sleep(1)
        self.browser.switch_to_window(self.browser.window_handles[-1])
        sleep(1)

    def test_search(self):
        print('test_search is being tested...')
        self.browser.get(self.config['Web']['web_google'])
        self.browser.maximize_window()

        sleep(1)

        searchColumn = self.browser.find_element_by_name('q')
        searchColumn.send_keys('one piece')
        searchColumn.submit()
        #searchBtn = self.browser.find_element_by_name('btnK')
        #searchBtn.click()
        #searchBtn.send_keys(Keys.RETURN)

    def test_linkText(self):
        print('test_linkText is being tested...')
        self.newWeb('python')
        self.browser.maximize_window()

        foundLinkText = self.browser.find_element_by_link_text('Docs')
        #print('@@', dir(foundLinkText))
        #foundLinkText.click()
        self.newTable(url=foundLinkText.get_attribute('href'))

    def test_xpath(self):
        self.newWeb('python')
        self.browser.maximize_window()

        sleep(1)

        #self.browser.find_element_by_xpath('//input[@id=\'id-search-field\']').send_keys('unittest')
        self.browser.find_element_by_xpath('//input[@name=\'q\']').send_keys('unittest')
        sleep(1)
        self.browser.find_element_by_name('submit').click()

    def test_newTab(self):
        print('test_newTab is being tested...')
        self.test_search()

        current_window = self.browser.current_window_handle
        print('@@ current window handle id:', current_window)

        sleep(1)

        # New tables
        #self.browser.execute_script('window.open(\'https://www.python.org/\')')
        self.newTable('youtube')
        self.newTable('python')
        self.newTable('yahoo')

        # Close tables from tail
        self.closeTable()       # close yahoo
        self.closeTable()       # close python

        #self.browser.switch_to_window(self.browser.window_handles[0])        
        self.browser.switch_to_window(current_window)        

if __name__ == '__main__':
    unittest.main()

