import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserDetails (models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    unique_id = models.UUIDField (default=uuid.uuid4, editable=False, unique=True)

@receiver(post_save, sender=User)
def create_user_profile (sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)