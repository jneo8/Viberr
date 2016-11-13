from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from pyvirtualdisplay import Display
import sys

class FunctionalTest(StaticLiveServerTestCase):
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
        self.browser.implicitly_wait(1)
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        # 使用 find_elements_  可以找到複數個tr標籤，再用迴圈去搜尋
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
