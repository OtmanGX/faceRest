# Generated by Django 2.2.13 on 2020-06-19 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faces', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facedetected',
            name='unknown_number',
        ),
    ]
