from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from .views import home_page
from .models import Item, List


class HomePageTest(TestCase):

    # 測試url /superlist/ 是否有連接到 homepage 這個function
    def test_root_url_resolvers(self):
        found = resolve('/superlist/')
        self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_html(self):
        # 建立HttpRequest物件
        request = HttpRequest()
        # 將request傳給home_page view, 會得到home_page回傳的response
        response = home_page(request)
        # 由於csrf token 所以會報錯
        expected_html = render_to_string('superlist/home.html')
        self.assertEqual(response.content.decode(), expected_html)
        # response.content是原始位元組，必須使用 b'' 語法來進行比較
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

# class ItemModelTest(TestCase):

#     def test_saving_and_retriving_items(self):

#         # 建立兩筆資料並儲存
#         first_item = Item()
#         first_item.text = 'The first(ever) list item'
#         first_item.save()

#         second_item = Item()
#         second_item.text = 'Item the second'
#         second_item.save()

#         # 撈出兩筆資料並比對text attrubite的值
#         save_items = Item.objects.all()
#         self.assertEqual(save_items.count(), 2)

#         first_save_item = save_items[0]
#         second_save_item = save_items[1]
#         self.assertEqual(first_save_item.text, 'The first(ever) list item')
#         self.assertEqual(second_save_item.text, 'Item the second')

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        save_list = List.objects.first()
        self.assertEqual(save_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_lists_template(self):
        list_ = List.objects.create()
        # response = self.client.get(reverse('/superlist/lists/%d/' % (list_.id,)))
        response = self.client.get(reverse('superlist:view_list', args=[list_.id], ))

        self.assertTemplateUsed(response, 'superlist/list.html')

    def test_display_all_item(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get(reverse('superlist:view_list', args=[list_.id],))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)



        response = self.client.get('/superlist/lists/%d/' % correct_list.id)
        # self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')





class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'item_text': 'A new list item'}
            )
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertEqual(response['location'], reverse('superlist:view_list', args=[new_list.id],))
       
    def test_redirects_after_POST(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'item_text': 'A new list item'}
            )
        new_list = List.objects.first()
        self.assertRedirects(response, reverse('superlist:view_list', args=[new_list.id], ))


