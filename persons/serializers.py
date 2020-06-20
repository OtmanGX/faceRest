from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.utils import json
import os
from .models import Person, Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name', 'persons']


class LabelSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class PersonSerializer(serializers.ModelSerializer):
    labels = LabelSerializer2(many=True, required=False)

    def run_validation(self, data=empty):
        # print(data)
        return super().run_validation(data)


    def create(self, validated_data):
        person = None
        if validated_data.get('labels', False):
            labels_raw = validated_data.pop('labels')
            labels = [Label.objects.get_or_create(name=label['name'])[0]
                      for label in labels_raw]

            person = Person.objects.create(**validated_data)
            person.labels.set(labels)
        if validated_data.get('matricule', False) in (False, ''):
            if not person :
                person = Person.objects.create(**validated_data)
            if person.matricule=='':
                person.matricule = person.name[:3].upper() +\
                    hex(person.id)[2:].upper()
            person.save()
        if person is not None:
            return person
        return super(PersonSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('labels', False):
            labels_raw = validated_data.pop('labels')
            labels = [Label.objects.get_or_create(name=label['name'])[0]
                      for label in labels_raw]

            person = super().update(instance, validated_data)
            person.labels.set(labels)
        else:
            person = super().update(instance, validated_data)

        return person

    class Meta:
        model = Person
        fields = '__all__'
        # fields = ['id', 'name', 'age', 'labels', 'active', 'created_at']
        depth = 1