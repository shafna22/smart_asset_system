from django.urls import path
from . import views

urlpatterns = [
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/edit/<int:id>/', views.edit_asset, name='edit_asset'),
    path('assets/delete/<int:id>/', views.delete_asset, name='delete_asset'),
]