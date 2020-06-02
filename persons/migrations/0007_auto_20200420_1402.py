# Generated by Django 2.2.12 on 2020-04-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0006_auto_20200420_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='labels',
        ),
        migrations.AddField(
            model_name='label',
            name='persons',
            field=models.ManyToManyField(blank=True, related_name='labels', to='persons.Person'),
        ),
    ]
