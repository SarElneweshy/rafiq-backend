from rest_framework import serializers
from ..models import Feeling


class FeelingSerializer(serializers.ModelSerializer):
    class Meta :
        model = Feeling
        fields = ("id", "emotion", "reason", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        user = self.context["request"].user
        return Feeling.objects.create(user=user, **validated_data)
