import factory
from django.utils.timezone import now
from factory.fuzzy import FuzzyChoice
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from accounts.models import Profile, Comment, Subscription


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    profile = factory.RelatedFactory(
        'accounts.tests.factories.ProfileFactory', factory_related_name='user'
    )


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
    avatar = factory.Faker('image_url')

    @factory.post_generation
    def bookmarks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for favorite in extracted:
                self.bookmarks.add(favorite)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(ProfileFactory)
    post = factory.SubFactory(
        'main.tests.factories.PostFactory'
    )
    text = factory.Faker('text')
    status = FuzzyChoice(choices=[True, True, True, False])
    created = factory.LazyAttribute(lambda x: now())


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    email = factory.Faker('email')
