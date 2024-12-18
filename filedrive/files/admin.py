from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin
from safedelete.admin import SafeDeleteAdminFilter
from safedelete.admin import highlight_deleted
from unfold.admin import ModelAdmin

from .models import SharedItem
from .models import UploadedItem


@admin.register(UploadedItem)
class UploadedItemAdmin(SafeDeleteAdmin, ModelAdmin):
    list_display = (
        highlight_deleted,
        "highlight_deleted_field",
        "owner",
        "name",
        "size",
    ) + SafeDeleteAdmin.list_display
    list_filter = ("owner", SafeDeleteAdminFilter) + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"


UploadedItemAdmin.highlight_deleted_field.short_description = UploadedItemAdmin.field_to_highlight


@admin.register(SharedItem)
class SharedItemAdmin(SafeDeleteAdmin, ModelAdmin):
    list_display = (
        highlight_deleted,
        "highlight_deleted_field",
        "item",
        "shared_with",
        "item__owner",
    ) + SafeDeleteAdmin.list_display
    list_filter = ("item__owner", "shared_with", SafeDeleteAdminFilter) + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"
