from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.utils.timezone import now

# Create your models here.

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return 'profil_img/{}/{}.{}'.format(instance.user.username, pid, extension)

class Profile(models.Model):
    Sex_type = (
        ('m', '남자'),
        ('w', '여자')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profil_img = ProcessedImageField(
        upload_to=user_path,
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality':60},
        blank='True',
        null='True'
    )
    name = models.CharField(max_length=50)
    about = models.TextField(max_length=500, blank=True)
    sex = models.CharField(choices=Sex_type, default='m', max_length=1)
    birth_date = models.DateField(null=True, blank=True)
    follow_set = models.ManyToManyField('self', blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username

    @property
    def get_follower(self):
        return [i.from_user for i in self.follower_user.all()]

    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()]

    @property
    def get_follower_count(self):
        return len(self.get_follower)

    @property
    def get_following_count(self):
        return len(self.get_following)



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Relation(models.Model):
    from_user = models.ForeignKey('Profile', related_name='follow_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey('Profile', related_name='follower_user', on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=now())

    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )