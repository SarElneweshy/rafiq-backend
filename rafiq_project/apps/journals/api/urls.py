from django.urls import path
from .views import JournalListCreateAPIView, JournalRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('', JournalListCreateAPIView.as_view(), name='journals-list-create'),
    path('<int:id>/', JournalRetrieveUpdateDeleteAPIView.as_view(), name='journals-rud'),
]