from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Profile(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    profilePicture = models.ImageField(null=True, default="saltbae.png")
    occupation = models.CharField(max_length=255, null=True)


class Blog(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.TextField()
    datePublished = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-datePublished']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
