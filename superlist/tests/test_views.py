from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.html import escape
# from unittest import skip
from ..models import Item, List
from ..forms import (
    ItemForm, EMPTY_ITEM_ERROR,
    ExistingListItemForm, DUPLICATE_ITEM_ERROR,
    )


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
            data={'text': text_1}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text_1)
        self.assertEqual(new_item.list, correct_list)

    # 測試 superlist:view_list Redirects 位置
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        text_1 = 'A new item for an existing list'
        response = self.client.post(
            reverse('superlist:view_list', args=[correct_list.id]),
            data={'text': text_1}
        )

        self.assertRedirects(response, reverse(
            'superlist:view_list', args=[correct_list.id]))
        
    # ItemForm 是否傳遞到html中
    def test_display_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(
            reverse('superlist:view_list', args=[list_.id]))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    #  POST 空白form
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            reverse('superlist:view_list', args=[list_.id]),
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_render_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superlist/list.html')

    def test_for_invaild_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    # 測試重複輸入項目
    def test_duplicate_item_validation_errors_end_up_on_list_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            reverse('superlist:view_list', args=[list1.id]),
            data={'text': 'textey'},
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'superlist/list.html')
        self.assertEqual(Item.objects.all().count(), 1)




class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'text': 'A new list item'}
        )
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertEqual(response['location'], reverse(
            'superlist:view_list', args=[new_list.id],))

    def test_redirects_after_POST(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'text': 'A new list item'})

        new_list = List.objects.first()
        self.assertRedirects(response, reverse(
            'superlist:view_list', args=[new_list.id], ))

    def test_vaildation_errors_are_sent_back_to_home_page_templates(self):
        response = self.client.post(
            reverse('superlist:new_list'),
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superlist/home.html')

        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(
            reverse('superlist:new_list'),
            data={'text': ''}
            )
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse('superlist:new_list'), data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superlist/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(reverse('superlist:new_list'), data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(reverse('superlist:new_list'), data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)










