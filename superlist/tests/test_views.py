from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.html import escape

from ..views import home_page
from ..models import Item, List
from ..forms import ItemForm


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_renders_home_templates(self):
        response =self.client.get(reverse('superlist:home'))
        # check used the correct html
        self.assertTemplateUsed(response, 'superlist/home.html')

    def test_home_page_user_item_form(self):
        response =self.client.get(reverse('superlist:home'))
        # check used the correct form
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_uses_lists_template(self):
        list_ = List.objects.create()
        response = self.client.get(
            reverse('superlist:view_list', args=[list_.id], ))

        self.assertTemplateUsed(response, 'superlist/list.html')

    # 測試correct_list 參數是否有傳進html
    def test_passes_correct_list_to_templates(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(
            reverse('superlist:view_list', args=[correct_list.id]),)
        self.assertEqual(response.context['list'], correct_list)

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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        text_1 = 'A new item for an existing list'
        self.client.post(
            reverse('superlist:view_list', args=[correct_list.id]),
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
            reverse('superlist:view_list', args=[correct_list.id]),
            data={'item_text': text_1}
        )

        self.assertRedirects(response, reverse(
            'superlist:view_list', args=[correct_list.id]))
    def test_vaildation_errors_end_up_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            reverse('superlist:view_list', args=[list_.id]),
            data={'item_text': ''},
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superlist/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


    
class NewListTest(TestCase):

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
            data={'item_text': 'A new list item'})

        new_list = List.objects.first()
        self.assertRedirects(response, reverse(
            'superlist:view_list', args=[new_list.id], ))

    def test_vaildation_errors_are_sent_back_to_home_page_templates(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superlist/home.html')

        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(
            reverse('superlist:new_list'),
            data={'item_text': ''}
            )
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)






