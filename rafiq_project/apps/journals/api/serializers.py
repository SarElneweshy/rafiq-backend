from rest_framework import serializers

class VoiceJournalSerializer(serializers.Serializer):
    content_voice = serializers.FileField()

class TextJournalSerializer(serializers.Serializer):
    content_text = serializers.CharField()

class SaveVoiceJournalSerializer(serializers.Serializer):
    content_text = serializers.CharField()
    detected_language = serializers.CharField(required=False)
    content_voice = serializers.FileField(required=False)