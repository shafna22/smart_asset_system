from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('user_management.urls')),  
    path('', include('inventory_management.urls')),  
    path('', include('asset_management.urls')),
    path('asset_assignment/', include('asset_assignment.urls')),
     path('tickets/', include('tickets.urls')),
]
