# Generated by Django 2.2.13 on 2020-07-07 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faces', '0004_auto_20200704_1008'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointage',
            options={'ordering': ['-id']},
        ),
    ]
