from rest_framework import serializers

from faces.models import FaceDetected, FaceDataSet, DATASET_TYPES
import os

class FaceDetectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceDetected
        fields = '__all__'
        depth = 1


class FaceDataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceDataSet
        fields = '__all__'

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        old_image_path = instance.image.path
        if(old_image_path):
            instance.image.save(os.path.basename(instance.image.name),
                                instance.image.file)
            print(validated_data.get("dataset_type"))
            print(instance.image.path)
            if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
        return instance

class MoveFaceSerializer(serializers.Serializer):
    id_person = serializers.IntegerField()
    id_face = serializers.ListField()
    dataset = serializers.ChoiceField(choices=DATASET_TYPES)

    def save(self, **kwargs):
        for id in self.validated_data.get('id_face'):
            face_detected = FaceDetected.objects.get(id=id)
            face_to_save = FaceDataSet.objects.create(
                label_id = self.validated_data.get('id_person'),
                dataset_type = self.validated_data.get('dataset'),
                image=face_detected.image
            )

            face_to_save.image.save(os.path.basename(face_to_save.image.name),
                                    face_to_save.image.file)
            face_detected.delete()
