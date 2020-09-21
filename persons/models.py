from django.db import models
import os
from facereco import PATH_TRAIN, PATH_TEST
from django.db.models.signals import pre_save
from django.dispatch import receiver
import shutil
from facereco.train.MFaceNet_LoadModel_SVM import save_labels, clean, total_train
from threading import Thread


def upload_image_path(instance, filename):
    return os.sep.join(["avatars", filename])


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
    last_time = models.DateTimeField(blank=False, null=True, default=None)
    # last_updated = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Temperature(models.Model):
    val = models.FloatField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(Person, related_name='temperatures', on_delete=models.CASCADE)


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
                if Person.objects.count() >= 2:
                    Thread(target=total_train).start()
                    # save_labels()


@receiver(models.signals.post_delete, sender=Person)
def auto_delete_file(sender, instance, **kwargs):
    print("signal delete")
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            instance.avatar.delete()
    try:
        paths = (os.path.join(PATH_TRAIN, instance.name),
                 os.path.join(PATH_TEST, instance.name))
        for path in paths:
            if os.path.exists(path):
                shutil.rmtree(path)
    except OSError:
        pass
    if Person.objects.count() < 2:
        print("smaller than 2")
        clean()
    else:
        Thread(target=total_train).start()


def rename_dataset(objs, new_name):
    for obj in objs:
        obj_split = obj.image.name.split(os.sep)
        obj_split[2] = new_name
        obj.image.name = os.path.join(*obj_split)
        obj.save()
