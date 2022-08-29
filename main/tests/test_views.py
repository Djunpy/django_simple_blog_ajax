from django.test import TestCase
from django.urls import reverse

from .factories import PostFactory, CategoryFactory, TagFactory
from accounts.tests.factories import ProfileFactory


class HomePageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = ProfileFactory()
        cls.category = CategoryFactory()
        cls.tags = TagFactory()
        cls.post = PostFactory(
            author=cls.author,
            category=cls.category,
            tags=cls.tags,
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('main:home-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '«The Zen of Python»')
        self.assertTemplateUsed(response, 'home_page.html')

    def test_post_detail_view(self):
        response = self.client.get(self.post.get_absolute_url())
        no_response = self.client.get('main:post-detail/567/')
        expected_string_title = self.post.title
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, expected_string_title)
        self.assertTemplateUsed(response, 'post-detail.html')

