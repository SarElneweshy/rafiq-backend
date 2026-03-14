from rest_framework import serializers
from apps.journals.models import Journal

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = [
            "id",
            "content",
            "dominant_emotion",
            
        ]
        read_only_fields = ["dominant_emotion", "created_at","language"]

    def validate_content(self, value):
        words = value.strip().split()
        if len(words) < 5:
            raise serializers.ValidationError("Journal entry must be at least 5 words.")
        if len(value) > 10000:
            raise serializers.ValidationError("Your journal entry is too long. ")
        return value
