from django.contrib import admin
from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "assigned_officer",
        "caller_phone",
        "address_text",
        "created_at",
        "accepted_at",
        "arrived_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("title", "details", "caller_phone", "address_text")
    ordering = ("-created_at",)

    # Edit sahifasida fieldlar tartibi
    fields = (
        "title",
        "details",
        "status",
        "assigned_officer",
        "address_text",
        "lat",
        "lng",
        "victim_first_name",
        "victim_last_name",
        "caller_phone",
        "created_by",
        "created_at",
        "accepted_at",
        "arrived_at",
        "closed_at",
    )

    # created_at ni edit qilolmasin (read-only)
    readonly_fields = ("created_at",)

    # Listda delete action bo‘lsin (checkbox → delete selected)
    actions = ["delete_selected"]
