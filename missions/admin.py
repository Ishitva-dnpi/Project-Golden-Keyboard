from django.contrib import admin

from .models import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("codename", "difficulty", "status", "hostel", "points", "deadline")
    list_filter = ("difficulty", "status", "hostel")
    search_fields = ("codename", "solver_handle")
