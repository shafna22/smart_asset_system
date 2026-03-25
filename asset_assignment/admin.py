from django.contrib import admin
from .models import AssetAssignment

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'assigned_date', 'return_date', 'is_returned')
    list_filter = ('is_returned', 'assigned_date', 'return_date')
    search_fields = ('asset__asset_id', 'asset__name', 'employee__username')
    ordering = ('assigned_date',)