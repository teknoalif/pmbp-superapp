from django.db import models
from django.contrib.auth.models import User

class Ekskul(models.Model):
    nama = models.CharField(max_length=100)
    pembina = models.ForeignKey(User, on_delete=models.CASCADE) # Akun Login
    nama_pembina = models.CharField(max_length=100) # Nama Lengkap (misal: Ust. Ahmad)
    jumlah_santri = models.IntegerField(default=0) # Kapasitas santri
    created_at = models.DateTimeField(auto_now_add=True) # Otomatis simpan waktu buat

    def __str__(self):
        return self.nama

class LaporanEkskul(models.Model):
    ekskul = models.ForeignKey(Ekskul, on_delete=models.CASCADE)
    tanggal = models.DateField()
    materi = models.TextField()
    dokumentasi = models.ImageField(upload_to='dokumentasi/', blank=True, null=True)
    jumlah_santri = models.IntegerField()
    diinput_pada = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.ekskul.nama} - {self.tanggal}"
