# Generated by Django 2.2.13 on 2020-07-04 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
        ('faces', '0002_remove_facedetected_unknown_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pointage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entree', models.DateTimeField()),
                ('date_sortie', models.DateTimeField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pointages', to='persons.Person')),
            ],
        ),
    ]
