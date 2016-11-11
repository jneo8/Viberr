from .base import FunctionalTest

class ItemVaildationTest(FunctionalTest):
    
    def test_can_add_empty_list_items(self):
        # user 前往首頁
        # self.browser.get('%s%s' % (self.server_url, '/superlist'))

        # 他在空白的清單項目內按下enter
        

        # homepage refresh，sent a error message
        # message say that can't be a space items

        # user try again, try to push some word in the item. Now it work!
        # user try to push space item again, the same error again.
        self.fail('write me!')


