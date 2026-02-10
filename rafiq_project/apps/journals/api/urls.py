from django.urls import path
from .views import VoiceJournalAPIView, TextJournalAPIView, SaveVoiceJournalAPIView

urlpatterns = [
    path("voice/", VoiceJournalAPIView.as_view()),
    path("voice/save/", SaveVoiceJournalAPIView.as_view()),
    path("text/", TextJournalAPIView.as_view()),

]