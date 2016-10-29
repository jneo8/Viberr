from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
# import unittest
import time



class NewVisitorTest(LiveServerTestCase):

    # browser = webdriver.Safari()

    def setUp(self):
        display = Display(visible=0, size=(800, 800))  
        display.start()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):    
        self.browser.get('%s%s' % (self.live_server_url, '/superlist'))
        # table = self.browser.find_element_by_id('id_list_table')


        # 網頁顯示出 To-Do
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Your To-Do lists', header_text)

        # user 受邀輸入一個代辦事項
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        # 在文字方塊輸入 'Buy peacock feathers'
        inputbox.send_keys('Buy peacock feathers')
        # 按下enter時網頁會更新，並列出 '1 : Buy peacock feathers'
        inputbox.send_keys(Keys.ENTER)
        # solution for StaleElementReferenceException
        time.sleep(2)
        # 檢查項目是否存在table中
        self.check_for_row_in_list_table('1: Buy peacock feathers')       

        # 此時仍然有另外一個文字方塊
        inputbox = self.browser.find_element_by_id('id_new_item')
        # user 輸入 'Use peacock feathers to make a fly'
        inputbox.send_keys('Use peacock feathers to make a fly')
        # POST and refresh page
        inputbox.send_keys(Keys.ENTER)
        # solution for StaleElementReferenceException
        time.sleep(2)

        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')       


       
        self.fail('finish the test!')

        # now user的清單有兩個項目
