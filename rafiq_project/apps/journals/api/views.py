import uuid
import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import JournalEntry
from .serializers import VoiceJournalSerializer,TextJournalSerializer,SaveVoiceJournalSerializer,JournalEntrySerializer

from ..services.whisper_service import transcribe_audio_file

class VoiceJournalAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VoiceJournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.validated_data["content_voice"]

        if audio.size > 5*1024*1024:
            return Response({"error": "File too large. Max 5MB."}, status=400)
        if not audio.name.endswith((".wav",".mp3",".m4a")):
            return Response({"error": "Unsupported file format."}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            for chunk in audio.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            text, detected_lang = transcribe_audio_file(tmp_path)
            return Response({
                "transcript": text, "detected_language": detected_lang
                })
            
        finally:
            os.remove(tmp_path)

class SaveVoiceJournalAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

        return Response({"message": "Journal saved successfully"}, status=201)

class TextJournalAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TextJournalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data["content_text"]
        

        if request.user.is_authenticated:
          
            entry = JournalEntry.objects.create(
                user=request.user,
                journal_type="text",
                content_text=text,
            )
            return Response({
                "message": "Text journal saved successfully"
            }, status=201)
        else:
            
            return Response({
                "text": text
            })

class JournalListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        journals = JournalEntry.objects.filter(user=request.user)
        serializer = JournalEntrySerializer(journals, many=True, context={"request": request})
        return Response({"message": "Your journals fetched successfully", "data": serializer.data})