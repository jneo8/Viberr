from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from ..views import home_page
from ..models import Item, List


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
        self.assertIn(b'<title>To-Do lists | Homepage</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))


class ListViewTest(TestCase):

    def test_uses_lists_template(self):
        list_ = List.objects.create()
        response = self.client.get(
            reverse('superlist:view_list', args=[list_.id], ))

        self.assertTemplateUsed(response, 'superlist/list.html')

    def test_display_all_item(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get(
            reverse('superlist:view_list', args=[list_.id],))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        response = self.client.get(
            reverse('superlist:view_list', args=[correct_list.id]))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')

    # 測試correct_list 參數是否有傳進html
    def test_passes_correct_list_to_templates(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(
            reverse('superlist:view_list', args=[correct_list.id]),)
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        text_1 = 'A new item for an existing list'
        self.client.post(
            reverse('superlist:add_item', args=[correct_list.id]),
            data={'item_text': text_1}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text_1)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        text_1 = 'A new item for an existing list'
        response = self.client.post(
            reverse('superlist:add_item', args=[correct_list.id]),
            data={'item_text': text_1}
        )

        self.assertRedirects(response, reverse(
            'superlist:view_list', args=[correct_list.id]))

    def test_saving_a_POST_request(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertEqual(response['location'], reverse(
            'superlist:view_list', args=[new_list.id],))

    def test_redirects_after_POST(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, reverse(
            'superlist:view_list', args=[new_list.id], ))
