from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Profile(models.Model):
    Sex_type = (
        ('m', '남자'),
        ('w', '여자')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    sex = models.CharField(choices=Sex_type, default='m', max_length=1)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()