from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from ..models import Item, List


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        # model save
        item = Item(list=list_, text='')
        # must get ValidationError
        with self.assertRaises(ValidationError):
            # model save won't get error
            item.save()
            # 手動執行完整驗證, because text(blank=False), it will get error
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()


    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # 應該不會error

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        word = 'some text'
        item = Item(text=word)
        self.assertEqual(str(item), word)


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), reverse(
            'superlist:view_list', args=[list_.id], ))
