from django import template

from main.models import Category, Tag


register = template.Library()


@register.inclusion_tag('include/category_tag.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('include/show_tags.html')
def show_tags():
    tags = Tag.objects.all()
    return {'tags': tags}