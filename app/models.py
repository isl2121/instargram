from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class App (models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField()
    content = models.CharField(max_length=500)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    created_time = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'app'
        verbose_name_plural = 'apps'

    def __str__(self):
        return self.title

    def save_app(self):
        return self.save()

    def like_count(self):
        return self.likes.count()
