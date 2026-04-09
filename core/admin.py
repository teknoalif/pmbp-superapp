from django.contrib import admin
from .models import Ekskul, LaporanEkskul # Pastikan di sini K-nya satu

# Ubah baris ini (sebelumnya Eskkul) menjadi:
admin.site.register(Ekskul)
admin.site.register(LaporanEkskul)
