from rest_framework import serializers
from apps.exercises.models import Disorder, Exercise

#first page serializer

class DisorderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = ['id', 'short_name', 'full_name']

#second page serializer
class ExerciseSerializer(serializers.ModelSerializer):
    detailed_exercises_list = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'title', 'short_desc', 'detailed_exercises_list', 'video_url']

    def get_detailed_exercises_list(self, obj):
        if obj.detailed_desc:
            return [line.strip() for line in obj.detailed_desc.split('\n') if line.strip()]
        return []

class DisorderDetailSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Disorder
        fields = [
            'exercises'
        ]




