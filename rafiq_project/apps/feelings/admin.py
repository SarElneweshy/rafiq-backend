from django.contrib import admin
from .models import Feeling


@admin.register(Feeling)
class FeelingAdmin(admin.ModelAdmin):
    list_display = ("user", "emotion", "created_at")
    list_filter = ("emotion", "created_at")
    search_fields = ("user__email", "reason")
