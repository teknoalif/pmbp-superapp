from django.shortcuts import render, redirect, get_object_or_404
from .models import Ekskul, LaporanEkskul
from .forms import LaporanForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages # 1. Tambah ini untuk Alert

# --- 1. FUNGSI REGISTRASI PAKET LENGKAP (USTADZ & EKSKUL) ---
def tambah_pembina_dan_ekskul(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)

        # Ambil data tambahan dari form HTML
        nama_ekskul = request.POST.get('nama_ekskul')
        nama_lengkap = request.POST.get('nama_lengkap') # 2. Ambil Nama Pembina
        jumlah_santri = request.POST.get('jumlah_santri') # 3. Ambil Jumlah Santri

        if user_form.is_valid() and nama_ekskul:
            user_baru = user_form.save()

            # Simpan ke model Ekskul dengan data lengkap
            Ekskul.objects.create(
                nama=nama_ekskul,
                pembina=user_baru,
                nama_pembina=nama_lengkap, # Simpan Nama Lengkap
                jumlah_santri=jumlah_santri # Simpan Jumlah Santri
            )

            # Munculkan Alert Berhasil
            messages.success(request, f'Alhamdulillah! Akun ustadz {nama_lengkap} dan unit {nama_ekskul} berhasil terdaftar.')
            return redirect('dashboard_admin')
    else:
        user_form = UserCreationForm()
    return render(request, 'tambah_pembina_ekskul.html', {'user_form': user_form})

# --- 2. FUNGSI DASHBOARD UTAMA (REKAP DATA) ---
def dashboard_admin(request):
    # Mengambil data laporan terbaru
    laporans = LaporanEkskul.objects.all().order_by('-tanggal')
    return render(request, 'dashboard_admin.html', {'laporans': laporans})

# --- 3. FUNGSI EDIT LAPORAN ---
def edit_laporan(request, pk):
    laporan = get_object_or_404(LaporanEkskul, pk=pk)
    if request.method == 'POST':
        form = LaporanForm(request.POST, request.FILES, instance=laporan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laporan berhasil diperbarui!')
            return redirect('dashboard_admin')
    else:
        form = LaporanForm(instance=laporan)
    return render(request, 'input.html', {'form': form, 'edit_mode': True})

# --- 4. FUNGSI HAPUS LAPORAN ---
def hapus_laporan(request, pk):
    laporan = get_object_or_404(LaporanEkskul, pk=pk)
    # Langsung hapus (sesuai logika tombol hapus di dashboard Kakak)
    laporan.delete()
    messages.warning(request, 'Laporan telah dihapus.')
    return redirect('dashboard_admin')

# --- 5. FUNGSI INPUT LAPORAN (UNTUK ASATIZ) ---
def input_laporan(request):
    if request.method == 'POST':
        form = LaporanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('halaman_sukses') # Diarahkan ke fungsi sukses
    else:
        form = LaporanForm()
    return render(request, 'input.html', {'form': form})

# --- 6. FUNGSI HALAMAN SUKSES ---
def halaman_sukses(request):
    return render(request, 'sukses.html')
