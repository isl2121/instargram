from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

import re, os

# Create your models here.
class App (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    '''
    image = ProcessedImageField(
        blank='True',
        null='True',
        processors=[Thumbnail(600, 600)],
        format='JPEG',
        options={'quality': 90}
    )
    '''
    photo = ProcessedImageField(
        processors=[Thumbnail(600, 600)],
        format='JPEG',
        options={'quality': 90},
        blank='True',
    )

    content = models.CharField(max_length=500)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    tag_setting = models.ManyToManyField('Tag', blank=True)
    created_time = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'app'
        verbose_name_plural = 'apps'

    def save(self, *args, **kwargs):
        super(App, self).save(*args, **kwargs)

        regex = r"\B#([a-z0-9가-힣ㄱ-ㅎ_]{2,})(?![~!@#$%^&*()=+_`\-\|\/'\[\]\{\}]|[?.,]*\w)"
        pattern = re.compile(regex)
        match = pattern.findall(self.content)

        for t in match:
            obj, tag = Tag.objects.get_or_create(tag=t)
            self.tag_setting.add(obj)

        return self

    def delete(self):
        try:
            os.remove(settings.BASE_DIR + self.image.url)
        except:
            pass
        return super(App, self).delete()


    def __str__(self):
        return self.title

    def save_app(self):
        return self.save()

    def like_count(self):
        return self.likes.count()


class Comment (models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.CharField(max_length=100)
    created_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reply

class Tag (models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reversed('app:get_tags', self.tag)