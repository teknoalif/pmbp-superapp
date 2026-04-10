from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'), # Menggunakan view kustom
    path('', views.input_laporan, name='input_laporan'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('registrasi-pembina/', views.tambah_pembina_dan_ekskul, name='tambah_pembina_ekskul'),
    path('edit/<int:pk>/', views.edit_laporan, name='edit_laporan'),
    path('hapus/<int:pk>/', views.hapus_laporan, name='hapus_laporan'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
