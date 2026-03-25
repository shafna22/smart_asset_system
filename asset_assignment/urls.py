from django.urls import path
from . import views

urlpatterns = [
    path('', views.assign_list, name='assign_list'),
    path('add/', views.assign_asset, name='assign_asset'),
    path('return/<int:id>/', views.return_asset, name='return_asset'),
     path('my-assets/', views.my_assets, name='my_assets'),

]