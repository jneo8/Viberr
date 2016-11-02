import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
# import unittest
import time


class NewVisitorTest(StaticLiveServerTestCase):

    # 啟動測試伺服器
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.server_url:
            super().tearDownClass()
    def setUp(self):
        display = Display(visible=0, size=(800, 800))
        display.start()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        # 使用 find_elements_  可以找到複數個tr標籤，再用迴圈去搜尋
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('%s%s' % (self.server_url, '/superlist'))
        # table = self.browser.find_element_by_id('id_list_table')

        # 網頁顯示出 To-Do
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start a new To-Do lists', header_text)

        # user1 受邀輸入一個代辦事項
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 在文字方塊輸入 'Buy peacock feathers'
        inputbox.send_keys('Buy peacock feathers')
        # 按下enter時會帶使用者到新的URL
        # 並且列出 1: Buy peacock feathers
        # 一個待辦清單的項目
        inputbox.send_keys(Keys.ENTER)
        user1_list_url = self.browser.current_url
        # 檢查 user1_list_url 是否匹配正規表達式
        self.assertRegex(user1_list_url, '/superlist/.+')
        # solution for StaleElementReferenceException
        time.sleep(2)
        # 檢查項目是否存在table中
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 此時仍然有另外一個文字方塊
        inputbox = self.browser.find_element_by_id('id_new_item')
        # user1 輸入 'Use peacock feathers to make a fly'
        inputbox.send_keys('Use peacock feathers to make a fly')
        # POST and refresh page
        inputbox.send_keys(Keys.ENTER)
        # solution for StaleElementReferenceException
        time.sleep(2)

        # 再次更新網頁並檢查是否有兩個項目
        self.check_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 然後換成新的使用者user2進來;這邊先關掉遊覽器
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # user2造訪首頁並且清單內無顯示任何user1的Item
        self.browser.get('%s%s' % (self.server_url, '/superlist'))
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # user2 輸入一個新的項目
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, 'superlist/.+')
        # 確認user1的網址和user2的網址不相同
        self.assertNotEqual(user1_list_url, user2_list_url)

        # 再次確認清單內沒有任何user1 的Item
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # self.fail('finish the test!')
    def test_layout_and_styling(self):
        # user 前往首頁
        self.browser.get('%s%s' % (self.server_url, '/superlist'))
        self.browser.set_window_size(1024, 768)

        # user發現輸入方塊被妥善置中
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width'] / 2,
            512,
            delta=5,
            )

        # user 開始編輯新清單
        # 發現這裡的inputbox 也置中
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width'] / 2,
            512,
            delta=5,
            )








