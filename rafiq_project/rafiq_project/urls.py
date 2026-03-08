from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Website HTML
    path("accounts/", include("apps.accounts.urls")),
    path("feelings/", include("apps.feelings.urls")),


    # API
    path("api/accounts/", include("apps.accounts.api.urls")),
    path("api/feelings/", include("apps.feelings.api.urls")),
    path("api/exercises/", include("apps.exercises.api.urls")),
    path("api/assessments/", include("apps.mental_assessment.api.urls")),
    path('api/notifications/', include('apps.notifications.api.urls')),
    path("api/journals/", include("apps.journals.api.urls")),
]

