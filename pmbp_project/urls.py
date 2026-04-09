from django.contrib import admin
from django.urls import path
from django.conf import settings # Tambahkan ini untuk akses settings
from django.conf.urls.static import static # Tambahkan ini untuk melayani file statis/media
# Import fungsi-fungsi dari views
from core.views import (
    input_laporan,
    dashboard_admin,
    tambah_pembina_dan_ekskul,
    edit_laporan,
    hapus_laporan,
    halaman_sukses # Pastikan ini di-import jika Kakak membuat view khusus sukses
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Halaman Input Laporan (Halaman Utama)
    path('', input_laporan, name='input_laporan'),

    # Halaman Sukses setelah Input (Opsional, jika ingin URL sendiri)
    # path('sukses/', halaman_sukses, name='sukses'),

    # Dashboard Utama (Pusat Kendali Kak Alif)
    path('dashboard/', dashboard_admin, name='dashboard_admin'),

    # Registrasi Paket Lengkap (Akun + Ekskul + Pembina)
    path('registrasi-pembina/', tambah_pembina_dan_ekskul, name='tambah_pembina_ekskul'),

    # Fitur Edit dan Hapus (Menggunakan ID/Primary Key)
    path('edit/<int:pk>/', edit_laporan, name='edit_laporan'),
    path('hapus/<int:pk>/', hapus_laporan, name='hapus_laporan'),
]

# PENTING: Sambungkan jalur untuk file Media (Gambar Dokumentasi)
# Agar saat Kakak klik thumbnail di Dashboard, gambarnya muncul
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
