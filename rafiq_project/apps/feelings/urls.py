from django.urls import path
from .views import FeelingView

urlpatterns = [
    path('', FeelingView.as_view(), name='feeling_page'),
]