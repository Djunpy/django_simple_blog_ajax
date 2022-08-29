from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managerse import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='avatar/%y/%m/%d')
    bookmarks = models.ManyToManyField('main.Post', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey('main.Post', on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментраий'
        verbose_name_plural = 'Коментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Subscription(models.Model):

    email = models.EmailField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-email',)

    def __str__(self):
        return self.email



