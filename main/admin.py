from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Tag
from accounts.models import Comment
from .forms import PostForm


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdminPanel(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'get_image', 'category', 'created', 'status', 'published')
    list_filter = ('author', 'category', 'tags', 'created', 'published', 'status')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('get_image',)
    list_editable = ('status',)
    inlines = [CommentInline]

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')


@admin.register(Category)
class CategoryAdminPanel(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdminPanel(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
