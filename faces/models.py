from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from persons.models import Person
import os

DATASET_TYPES = [('Train', 'train'), ('Test', 'test')]


def upload_image_path(instance, filename):
    if isinstance(instance, FaceDetected):
        return os.sep.join(["detected", instance.label.name, filename])
    else:
        return os.sep.join(["dataset" + instance.model, instance.dataset_type.lower(),
                            instance.label.name, filename])


class Pointage(models.Model):
    person = models.ForeignKey(Person, related_name='pointages', on_delete=models.CASCADE)
    date_entree = models.DateTimeField(null=True)
    date_sortie = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-id']


class FaceDetected(models.Model):
    image = models.ImageField(blank=True, upload_to=upload_image_path)
    label = models.ForeignKey(Person, related_name='faces', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    instate = models.BooleanField(default=True)
    precision = models.FloatField(blank=True)

    class Meta:
        ordering = ['-created_at']


class FaceDataSet(models.Model):
    image = models.ImageField(blank=True, upload_to=upload_image_path)
    label = models.ForeignKey(Person, related_name='faces_dataset', on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dataset_type = models.CharField(choices=DATASET_TYPES, default='train', max_length=10)
    model = models.CharField(max_length=35, default="", blank=True)

    class Meta:
        ordering = ['created_at']


# def auto_delete_file(sender, instance, **kwargs):
#     print("receiver called")
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             instance.image.delete()

# post_delete.connect(auto_delete_file, sender='faces.')

@receiver(models.signals.post_delete, sender=FaceDetected)
def auto_delete_file_detected(sender, instance, **kwargs):
    # print("receiver called")
    if instance.image:
        if os.path.isfile(instance.image.path):
            instance.image.delete(False)


# @receiver(models.signals.post_delete, sender=FaceDetected)


@receiver(models.signals.post_delete, sender=FaceDataSet)
def auto_delete_file(sender, instance, **kwargs):
    # print("receiver called")
    if instance.image:
        if os.path.isfile(instance.image.path):
            instance.image.delete(False)

#
# @receiver(models.signals.pre_save, sender=FaceDataSet)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = FaceDataSet.objects.get(pk=instance.pk).image
#     except FaceDataSet.DoesNotExist:
#         return False
#
#     instance.image.save(os.path.basename(instance.image.name),
#                         instance.image.file)
#     new_file = instance.image
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
