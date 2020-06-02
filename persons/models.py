from django.db import models
import os

from django.dispatch import receiver


def upload_image_path(instance, filename):
    return os.sep.join(["avatars", filename]);


class Label(models.Model):
    name = models.CharField(max_length=25, null=False)


class Person(models.Model):
    name = models.CharField(max_length=35, blank=False, unique=True)
    avatar = models.ImageField(blank=True, upload_to=upload_image_path)
    matricule = models.CharField(max_length=12, unique=True, null=True, blank=True)
    age = models.SmallIntegerField(blank=True, null=True)
    labels = models.ManyToManyField(Label, related_name='persons', blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_delete, sender = Person)
def auto_delete_file(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            instance.avatar.delete()
