from django.contrib import admin
from .models import TeamModels
# ======================================================================================================================
# مدیریت اعضای تیم
@admin.register(TeamModels)
class TeamModelsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "position",
        "phone",
        "is_active",
        "is_manager",
    )

    search_fields = (
        "full_name",
        "position",
    )

    list_filter = (
        "is_active",
    )

    list_display_links = (
        "id",
        "full_name",
    )

    ordering = (
        "id",
    )
# ======================================================================================================================