import os

# Fungsi untuk membuat file secara otomatis dengan isi kodenya
def buat_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"[OK] File dibuat: {path}")

# 1. Membuat struktur folder dasar Django
print("--- Memulai Setup Proyek PMBP Al Binaa ---")
os.system('pip install django') # Memastikan Django terinstall
os.system('django-admin startproject pmbp_project .') # Membuat proyek utama
os.system('python manage.py startapp core') # Membuat aplikasi core untuk laporan

# 2. Membuat isi MODELS (Database)
models_code = """from django.db import models
from django.contrib.auth.models import User

class Ekskul(models.Model):
    nama = models.CharField(max_length=100)
    pembina = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nama

class LaporanEkskul(models.Model):
    ekskul = models.ForeignKey(Eskkul, on_delete=models.CASCADE)
    tanggal = models.DateField()
    materi = models.TextField()
    dokumentasi = models.ImageField(upload_to='laporan_foto/', blank=True)
    jumlah_santri = models.IntegerField()
    diinput_pada = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.ekskul.nama} - {self.tanggal}"
"""
buat_file('core/models.py', models_code)

# 3. Membuat isi FORMS (Tampilan Input)
forms_code = """from django import forms
from .models import LaporanEkskul

class LaporanForm(forms.ModelForm):
    class Meta:
        model = LaporanEkskul
        fields = ['ekskul', 'tanggal', 'materi', 'dokumentasi', 'jumlah_santri']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'materi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'jumlah_santri': forms.NumberInput(attrs={'class': 'form-control'}),
            'ekskul': forms.Select(attrs={'class': 'form-control'}),
        }
"""
buat_file('core/forms.py', forms_code)

# 4. Membuat isi VIEWS (Logika Input)
views_code = """from django.shortcuts import render
from .forms import LaporanForm

def input_laporan(request):
    if request.method == 'POST':
        form = LaporanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'sukses.html')
    else:
        form = LaporanForm()
    return render(request, 'input.html', {'form': form})
"""
buat_file('core/views.py', views_code)

# 5. Registrasi ke ADMIN agar Kak Alif bisa lihat rekapnya
admin_code = """from django.contrib import admin
from .models import Ekskul, LaporanEkskul

admin.site.register(Eskkul)
admin.site.register(LaporanEkskul)
"""
buat_file('core/admin.py', admin_code)

# 6. Menjalankan migrasi database awal
print("\\n--- Menyiapkan Database ---")
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

print("\\n--- SETUP SELESAI ---")
print("Silakan jalankan: python manage.py runserver")
