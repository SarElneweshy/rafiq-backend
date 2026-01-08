from django.urls import path
from .views.general_views import GeneralTestApiView, TestResultsApiView
from .views.depression_views import DepressionTestApiView
urlpatterns = [
    # General Test API Endpoints #
    path("general-test/predict/", GeneralTestApiView.as_view(), name="api_predict"),
    path("general-test/results/", TestResultsApiView.as_view(), name="api_results"),
    # Depression Test API Endpoint #

    path("depression-test/predict/", DepressionTestApiView.as_view(), name="api_depression_predict"),
]
