from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # admin panel kütüphanesi
    path('', include('shop.urls', namespace='shop')),
]