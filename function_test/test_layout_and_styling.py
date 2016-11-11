from .base import FunctionalTest

class LayoutAndsytlingTest(FunctionalTest):

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