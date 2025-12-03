from rest_framework import serializers
from apps.exercises.models import Disorder, Exercise

#first page serializer

class DisorderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = ['id', 'short_name', 'full_name']

#second page serializer
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'short_desc', 'detailed_desc', 'video_url']

class DisorderDetailSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Disorder
        fields = [
            'id',
            'short_name',
            'exercises'
        ]




