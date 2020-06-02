from django.db import models
from django.dispatch import receiver
from persons.models import Person
import os

DATASET_TYPES = [('Train', 'train'), ('Test', 'test')]


def upload_image_path(instance, filename):
    if isinstance(instance, FaceDetected):
        return os.sep.join(["detected", instance.label.name, filename])
    else:
        return os.sep.join(["dataset", instance.dataset_type.lower(),
                            instance.label.name, filename]);


class FaceDetected(models.Model):
    image = models.ImageField(blank=True, upload_to=upload_image_path)
    label = models.ForeignKey(Person, related_name='faces', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    precision = models.FloatField(blank=True)
    unknown_number = models.SmallIntegerField(blank=True, default=0)

    class Meta:
        ordering = ['created_at']


class FaceDataSet(models.Model):
    image = models.ImageField(blank=True, upload_to=upload_image_path)
    label = models.ForeignKey(Person, related_name='faces_dataset', on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dataset_type = models.CharField(choices=DATASET_TYPES, default='train', max_length=10)

    class Meta:
        ordering = ['created_at']


@receiver(models.signals.post_delete, sender=FaceDetected)
def auto_delete_file(sender, instance, **kwargs):
    print("receiver called")
    if instance.image:
        if os.path.isfile(instance.image.path):
            instance.image.delete()


@receiver(models.signals.post_delete, sender=FaceDataSet)
def auto_delete_file(sender, instance, **kwargs):
    print("receiver called")
    if instance.image:
        if os.path.isfile(instance.image.path):
            instance.image.delete()

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
