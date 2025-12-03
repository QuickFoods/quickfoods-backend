# core/admin.py
from django.contrib import admin
from .models import Store, Deal, FreshItem


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city")
    search_fields = ("name", "code", "city")


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "segment", "category", "store", "is_active", "show_on_home")
    list_filter = ("segment", "category", "store", "is_active", "show_on_home")
    search_fields = ("title", "tag", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(FreshItem)
class FreshItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "store", "price_label", "is_active")
    list_filter = ("category", "store", "is_active")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
