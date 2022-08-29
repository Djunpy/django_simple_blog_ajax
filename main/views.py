from django.core import serializers
from django.shortcuts import render, get_object_or_404
import datetime
from django.db.models import F
from django.views import generic
from django.http import JsonResponse
import json
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

from .models import Post, Category


class HomePageView(generic.View):
    model = Post
    template_name = 'home_page.html'
    paginator = Paginator

    def get(self, request, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            page_number = request.GET.get('page')
            paginator_obj = self.paginator(self.get_object_list(), 4)
            try:
                page = paginator_obj.get_page(page_number)
            except PageNotAnInteger:
                page = paginator_obj.get_page(1)
            except EmptyPage:
                pass
            posts = []
            for obj in page:
                item = {
                    'id': obj.pk,
                    'author_name': obj.author.user.username,
                    'author_avatar': obj.author.avatar.url,
                    'title': obj.title,
                    'image': obj.image.url,
                    'description': obj.description[:80],
                    'category': obj.category.name,
                    # 'tags': [tag.name for tag in obj.get_tags],
                    'views': obj.views,
                    'published': obj.published.strftime('%d.%m.%Y'),
                }
                posts.append(item)
            context = {
                'object_list': posts,
            }
            return JsonResponse(context, status=200)
        return render(request, self.template_name)

    def get_object_list(self):
        objects = self.model.objects.select_related('category', 'author').filter(status=True)
        return objects


class ByCategory(HomePageView):

    def get_object_list(self):
        objects = self.model.objects.select_related('category', 'author').filter(category_id=self.kwargs['category_id'], status=True)
        return objects


class PostDetailView(generic.DetailView):
    # model = Post
    template_name = 'post-detail.html'
    queryset = Post.objects.select_related('category').prefetch_related('tags').filter(status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


def search_results(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        search_data = json.load(request)['q']
        qs = Post.objects.filter(title__icontains=search_data, status=True)

        if qs.exists() and len(search_data) > 0:
            result = []
            for obj in qs:
                item = {
                    'id': obj.pk,
                    'title': obj.title,
                    'image': obj.image.url,
                }
                result.append(item)
            return JsonResponse({'search_data': result}, status=200)
    return JsonResponse({'err': 'Error'})


