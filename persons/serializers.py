from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.utils import json

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

    # def to_internal_value(self, data):
    #     if isinstance(data['labels'],str):
    #         data['labels'] = json.loads(data['labels'])
    #     print(data)
    #     return super().to_internal_value(data)

    def run_validation(self, data=empty):
        # print(data)
        return super().run_validation(data)

    # def validate_labels(self, value):
    #     print(value)
    #     if isinstance(value, str):
    #         value = json.loads(value)
    #     print(value)
    #     return value

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


    class Meta:
        model = Person
        fields = '__all__'
        # fields = ['id', 'name', 'age', 'labels', 'active', 'created_at']
        depth = 1