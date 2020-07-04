from django.db import models
import os
from facereco import PATH_TRAIN, PATH_TEST
from django.db.models.signals import pre_save
from django.dispatch import receiver
import shutil
from facereco.train.MFaceNet_LoadModel_SVM import save_labels, clean


def upload_image_path(instance, filename):
    return os.sep.join(["avatars", filename]);


class Label(models.Model):
    name = models.CharField(max_length=25, null=False)


class Person(models.Model):
    name = models.CharField(max_length=35, blank=False, unique=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_image_path)
    matricule = models.CharField(max_length=12, unique=True, null=True, blank=True)
    age = models.SmallIntegerField(blank=True, null=True)
    unknown = models.BooleanField(default=False)
    unknown_number = models.SmallIntegerField(default=0, null=True)
    labels = models.ManyToManyField(Label, related_name='persons', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=Person, dispatch_uid="update_person_name")
def auto_rename_dataset(sender, instance, **kwargs):
    pk = instance.pk
    if pk:
        person = Person.objects.get(pk=instance.pk)
        if instance.name != person.name:
            instance.unknown = False
            new_name = instance.name
            if new_name != person.name:
                try:
                    os.rename(os.path.join(PATH_TRAIN, person.name),
                              os.path.join(PATH_TRAIN, new_name))
                    os.rename(os.path.join(PATH_TEST, person.name),
                              os.path.join(PATH_TEST, new_name))
                except Exception:
                    pass
                rename_dataset(instance.faces_dataset.all(), new_name)
                save_labels()


@receiver(models.signals.post_delete, sender=Person)
def auto_delete_file(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            instance.avatar.delete()
    try:
        shutil.rmtree(os.path.join(PATH_TRAIN, instance.name))
        shutil.rmtree(os.path.join(PATH_TEST, instance.name))
    except FileNotFoundError:
        pass
    if Person.objects.count() < 2:
        print("smaller than 2")
        clean()
    else:
        save_labels()


def rename_dataset(objs, new_name):
    for obj in objs:
        obj_split = obj.image.name.split(os.sep)
        print(obj_split)
        obj_split[2] = new_name
        obj.image.name = os.path.join(*obj_split)
        print(obj.image.name)
        obj.save()
