"""Signal handlers for StudyBuddy user profile files."""

import os

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def delete_old_profile_picture(sender, instance, **kwargs):
    """Remove the previous profile picture when a user uploads a new one."""

    if instance.pk:
        old_profile_picture = sender.objects.get(pk=instance.pk).profile_picture
        if old_profile_picture:
            if old_profile_picture != instance.profile_picture:
                if os.path.isfile(old_profile_picture.path):
                    os.remove(old_profile_picture.path)
