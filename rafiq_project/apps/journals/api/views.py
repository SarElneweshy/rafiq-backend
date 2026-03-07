from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from apps.journals.models import Journal
from .serializers import JournalSerializer
from apps.journals.services.emotion import analyze_emotion

class JournalListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JournalSerializer

    def get_queryset(self): 
        return Journal.objects.filter(user=self.request.user).order_by('-created_at')
    
    #------- create journal -------#

    def perform_create(self, serializer):
        content = self.request.data.get("content", "").strip()
        emotions, dominant = analyze_emotion(content)

        if dominant == "Unsupported Language":
            raise ValidationError({
                "language_error": "This language is not supported. Please write in English."
            })

        self.journal = serializer.save(
            user=self.request.user,
            language="en",
            emotions=emotions,
            dominant_emotion=dominant
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({
            "message": "Your journal saved successfully ",
            "dominant_emotion": self.journal.dominant_emotion
        }, status=status.HTTP_201_CREATED)

class JournalRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JournalSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)
    
    #------ retrieve journal -------#

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({
            "message": "Journal fetched successfully ",
            "data": self.get_serializer(instance).data
        })
    
    #------ update journal -------#

    def perform_update(self, serializer):
        old_content = serializer.instance.content
        new_content = self.request.data.get(
            "content",
            old_content
        ).strip()

        if new_content != old_content:
            emotions, dominant = analyze_emotion(new_content)
            if dominant == "Unsupported Language":
                raise ValidationError({
                    "language_error": "Update failed. Only English is supported."
                })
        else:
            emotions = serializer.instance.emotions
            dominant = serializer.instance.dominant_emotion

        self.journal = serializer.save(
            content=new_content,
            emotions=emotions,
            dominant_emotion=dominant
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response({
            "message": "Journal updated successfully ",
            "dominant_emotion": self.journal.dominant_emotion
        })
    
    #------ delete journal -------#
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "message": "Journal deleted successfully "
        }, status=status.HTTP_204_NO_CONTENT)
    