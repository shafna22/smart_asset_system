from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'availability')  # Columns shown in admin list view
    list_filter = ('quantity',)  # Add a filter by quantity
    search_fields = ('item_name',)  # Search by item name
    ordering = ('item_name',)  # Default ordering