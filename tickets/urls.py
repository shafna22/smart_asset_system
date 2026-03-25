from django.urls import path
from . import views

urlpatterns = [
    path('raise/', views.raise_ticket, name='raise_ticket'),
     path('my-tickets/', views.ticket_list, name='ticket_list'),
    path('admin-tickets/', views.admin_ticket_list, name='admin_ticket_list'),
    path('update-ticket/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
]