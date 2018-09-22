from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('items/', include('groceries.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
