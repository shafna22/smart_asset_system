from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'name', 'brand', 'inventory_item', 'status')  # Columns in list view
    list_filter = ('status', 'brand')  # Filter by status and brand
    search_fields = ('asset_id', 'name', 'brand')  # Search by asset_id, name, or brand
    ordering = ('asset_id',)  # Default ordering