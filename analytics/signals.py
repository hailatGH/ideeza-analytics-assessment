from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import Profile


@receiver(
    post_save, sender=User
)  # fires on user create to ensure a profile is created for each user
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(
    post_save, sender=User
)  # fires on user save to ensure data sync between user and profile
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
