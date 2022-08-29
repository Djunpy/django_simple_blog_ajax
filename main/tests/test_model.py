from django.test import TestCase

from .factories import TagFactory, CategoryFactory, PostFactory
from accounts.tests.factories import ProfileFactory


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()

    def test_string_representation(self):
        category = self.category
        expected_string_name = category.name
        self.assertEqual(str(category), expected_string_name)


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = TagFactory()

    def test_string_representation(self):
        tag = self.tag
        expected_string_name = tag.name
        self.assertEqual(str(tag), expected_string_name)


class PostModelTest(TestCase):
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

    def test_string_representation(self):
        post = self.post
        expected_string_title = post.title
        self.assertEqual(str(post), expected_string_title)