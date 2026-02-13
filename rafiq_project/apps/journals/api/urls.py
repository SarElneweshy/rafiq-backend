from django.urls import path
from .views import (
    VoiceJournalAPIView,
    SaveVoiceJournalAPIView,
    TextJournalAPIView,
    JournalListAPIView
)

urlpatterns = [
    path("voice/", VoiceJournalAPIView.as_view()),
    path("voice/save/", SaveVoiceJournalAPIView.as_view()),
    path("text/", TextJournalAPIView.as_view()),
    path("history/", JournalListAPIView.as_view()),
]