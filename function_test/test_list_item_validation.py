from .base import FunctionalTest

class ItemVaildationTest(FunctionalTest):


    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')


    # 測試 ItemForm 空白項目error
    def test_can_add_empty_list_items(self):
        # user 前往首頁
        self.browser.get('%s%s' % (self.server_url, '/superlist'))
        self.get_item_input_box().send_keys('\n')

        # 他在空白的清單項目內按下enter
        # homepage refresh，sent a error message
        # message say that can't be a space items
        error = self.get_error_element()
        error_message = "You can't have an empty list item"
        self.assertEqual(error.text, error_message)
        

        # user try again, try to push some word in the item. Now it work!
        word_1  = 'Buy milk'
        self.get_item_input_box().send_keys('%s\n' % word_1)
        self.check_for_row_in_list_table('1: %s' % word_1)

        # user try to send blank item again, get same error again.
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()

        self.assertEqual(error.text, error_message)

        # user can send some word to fix it.
        word_2 = 'Make tea'
        self.get_item_input_box().send_keys('%s\n' % word_2)
        self.check_for_row_in_list_table('1: %s' % word_1)
        self.check_for_row_in_list_table('2: %s' % word_2)

    # 測試 ItemForm 重複項目 error
    def test_cannot_add_duplicate_items(self):
        # user前往首頁逼見新的清單

        self.browser.get('%s%s' % (self.server_url, '/superlist'))
        word_1 = 'Buy willies'
        self.get_item_input_box().send_keys('%s\n' % word_1)
        self.check_for_row_in_list_table('1: %s' % word_1)

        #user 輸入另一個相同項目
        self.get_item_input_box().send_keys('%s\n' % word_1)

        self.check_for_row_in_list_table('1: %s' % word_1)

        error = self.get_error_element()
        error_message = "You've already got this in your list"
        self.assertEqual(error.text, error_message)

    def test_error_message_are_cleared_on_input(self):
        self.browser.get('%s%s' % (self.server_url, '/superlist'))

        # input blank text, get error
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        # 是否可見
        self.assertTrue(error.is_displayed())

        # put some text and get no error
        self.get_item_input_box().send_keys('a')
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
























