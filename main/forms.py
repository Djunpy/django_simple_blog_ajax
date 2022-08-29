from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'