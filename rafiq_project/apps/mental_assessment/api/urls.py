from django.urls import path
from .views import GeneralTestApiView, TestResultsApiView

urlpatterns = [
    path("general-test/predict/", GeneralTestApiView.as_view(), name="api_predict"),
    path("general-test/results/", TestResultsApiView.as_view(), name="api_results"),
]
