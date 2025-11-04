from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),           # HTML pages
    path('api/accounts/', include('apps.accounts.api.urls')), # API endpoints
    path('api/', include('apps.feelings.api.urls')),
    path('feelings/', include('apps.feelings.urls')),
]