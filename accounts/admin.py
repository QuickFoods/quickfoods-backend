# accounts/admin.py
from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "barcode", "points", "store_id", "created_at")
    search_fields = ("user__username", "barcode")
    list_filter = ("store_id",)
    readonly_fields = ("barcode", "created_at")
