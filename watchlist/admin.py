from django.contrib import admin

from .models import WatchItem


@admin.register(WatchItem)
class WatchItemAdmin(admin.ModelAdmin):
    list_display = ("title", "item_type", "genre", "status", "rating", "user", "created_at")
    list_filter = ("status", "item_type", "genre")
    search_fields = ("title", "user__username")
    ordering = ("-created_at",)

# Register your models here.
