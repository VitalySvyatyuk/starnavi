from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, help_text='Email')
    email_deliverability = models.CharField(max_length=30, default='unchecked')
    enrichment = JSONField(default=dict)

    def __str__(self):
        return self.email


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('user', 'title',)
        ordering = ('-created',)


class Preference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} for post {}. Preference by {}".format(self.like, self.post.title, self.user.username)

    class Meta:
        unique_together = ('user', 'post',)
        ordering = ('-date',)
