from django.contrib.auth.models import User  # Imports the built-in User model, which is the sender
from django.db.models.signals import post_save  # Imports the post_save signal when creating a user
from django.dispatch import receiver  # Import receiver

from .models import Profile  # Profile model


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
