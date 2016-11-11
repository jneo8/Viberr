from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from ..models import Item, List


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

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        # model save
        item = Item(list=list_, text='')
        # must get ValidationError
        with self.assertRaises(ValidationError):
            # model save won't get error
            #
            item.save()
            # 手動執行完整驗證, because text(blank=False), it will get error
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), reverse(
            'superlist:view_list', args=[list_.id], ))
        
