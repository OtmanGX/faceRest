# Generated by Django 2.2.13 on 2020-08-19 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='person',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
