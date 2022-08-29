from django.test import TestCase
from django.contrib.auth import get_user_model
from .factories import UserFactory, ProfileFactory, CommentFactory, SubscriptionFactory

User = get_user_model()
from main.tests.factories import PostFactory


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_string_representation(self):
        user = self.user
        expected_string_email = user.email
        self.assertEqual(str(user), expected_string_email)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()

    def test_string_representation(self):
        profile = self.profile
        expected_string = profile.user.username
        self.assertEqual(str(profile), expected_string)


class CommentModelTest(TestCase):
    def setUp(self):
        self.author = ProfileFactory()
        self.post = PostFactory()
        self.comment = CommentFactory(author=self.author, post=self.post)

    def test_string_representation(self):
        comment = self.comment
        expected_string = comment.text
        self.assertEqual(str(comment), expected_string)


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.subscription = SubscriptionFactory()

    def test_string_representation(self):
        subscription = self.subscription
        expected_string = subscription.email
        self.assertEqual(str(subscription), expected_string)