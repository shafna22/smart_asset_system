from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'employee', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'asset')
    search_fields = ('asset__asset_id', 'asset__name', 'employee__username', 'issue_description')
    ordering = ('-created_at',)