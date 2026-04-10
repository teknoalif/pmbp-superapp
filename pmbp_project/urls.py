from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('input/', views.input_laporan, name='input_laporan'),
    path('accounts/', include('django.contrib.auth.urls')),
]