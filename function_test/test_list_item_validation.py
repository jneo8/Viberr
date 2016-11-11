from .base import FunctionalTest

class ItemVaildationTest(FunctionalTest):
    
    def test_can_add_empty_list_items(self):
        # user 前往首頁
        self.browser.get('%s%s' % (self.server_url, '/superlist'))
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 他在空白的清單項目內按下enter
        # homepage refresh，sent a error message
        # message say that can't be a space items
        error = self.browser.find_element_by_css_selector('.has-error')
        error_message = "You can't have an empty list item"
        self.assertEqual(error.text, error_message)
        

        # user try again, try to push some word in the item. Now it work!
        word_1  = 'Buy milk'
        self.browser.find_element_by_id('id_new_item').send_keys('%s\n' % word_1)
        self.check_for_row_in_list_table('1: %s' % word_1)

        # user try to send blank item again, get same error again.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has-error')

        self.assertEqual(error.text, error_message)

        # user can send some word to fix it.
        word_2 = 'Make tea'
        self.browser.find_element_by_id('id_new_item').send_keys()
        self.check_for_row_in_list_table('1: %s' % word_1)
        self.check_for_row_in_list_table('2: %s' % word_2)



        self.fail('write me!')


