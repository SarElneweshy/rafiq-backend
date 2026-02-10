import uuid
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..models import JournalEntry
from .serializers import VoiceJournalSerializer, TextJournalSerializer, SaveVoiceJournalSerializer
from ..services.whisper_service import transcribe_audio_file
import tempfile


class VoiceJournalAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VoiceJournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio = serializer.validated_data["content_voice"]

        # 🔐 Security checks
        if audio.size > 5 * 1024 * 1024:
            return Response({"error": "File too large"}, status=400)

        if not audio.name.endswith((".wav", ".mp3", ".m4a")):
            return Response({"error": "Unsupported file format"}, status=400)

        
        # Save the file temporarily

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            for chunk in audio.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            text, detected_lang = transcribe_audio_file(tmp_path)
            return Response({
                "transcript": text,
                "detected_language": detected_lang
            })
        
        finally:
            os.remove(tmp_path)

class SaveVoiceJournalAPIView(APIView):
    """
    Save voice journal AFTER user edits transcript
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=401
            )

        serializer = SaveVoiceJournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry = JournalEntry.objects.create(
            user=request.user,
            journal_type="voice",
            content_text=serializer.validated_data["content_text"],
            detected_language=serializer.validated_data.get("detected_language"),
        )

        if "content_voice" in serializer.validated_data:
            entry.content_voice.save(
                serializer.validated_data["content_voice"].name,
                serializer.validated_data["content_voice"]
            )

        return Response({
            "message": "Journal saved successfully",
            "id": entry.id
        })


class TextJournalAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TextJournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["content_text"]

        saved = False
        if request.user.is_authenticated:
            JournalEntry.objects.create(
                user=request.user,
                journal_type="text",
                content_text=text,
            )
            saved = True

        return Response({
            "text": text,
            "saved": saved
        })