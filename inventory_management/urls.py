from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),
    path('inventory/edit/<int:id>/', views.edit_inventory, name='edit_inventory'),
    path('inventory/delete/<int:id>/', views.delete_inventory, name='delete_inventory'),
]