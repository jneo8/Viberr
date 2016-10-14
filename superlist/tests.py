from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page


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
        expected_html = render_to_string('superlist/home.html')
        self.assertEqual(response.content.decode(), expected_html)
        # response.content是原始位元組，必須使用 b'' 語法來進行比較
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
