import random
import factory
from django.utils.text import slugify
from factory.fuzzy import FuzzyInteger, FuzzyChoice
from django.utils.timezone import now

from accounts.tests.factories import ProfileFactory
from main.models import Category, Tag, Post


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('sentence')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('sentence')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(ProfileFactory)
    title = factory.Faker('sentence')
    image = factory.Faker('image_url')
    description = factory.Faker('text')
    category = factory.SubFactory(CategoryFactory)
    views = FuzzyInteger(0, 45)
    tags = factory.RelatedFactoryList(
        TagFactory,
        factory_related_name='post',
        size=lambda: random.randint(1, 5)
    )
    created = factory.LazyFunction(now)
    updated = factory.LazyAttribute(lambda x: now())
    published = factory.LazyAttribute(lambda x: now())
    status = FuzzyChoice(choices=[True, True, True, False])

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)