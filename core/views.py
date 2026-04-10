from django.shortcuts import render, redirect, get_object_or_404
from .models import Ekskul, LaporanEkskul
from .forms import LaporanForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import gspread
from google.oauth2.service_account import Credentials
import os

# --- FIX LOGOUT 405 ---
def logout_view(request):
    logout(request)
    return redirect('login')

# --- FUNGSI SINKRONISASI (DEBUG MODE) ---
def sync_to_sheets(laporan, user_obj):
    print("--- Memulai Proses Sinkronisasi ---")
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Cari file key di folder project
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_key = os.path.join(base_dir, "google_key.json")
        print(f"Mencari key di: {path_key}")
        
        if not os.path.exists(path_key):
            print("EROR: File google_key.json TIDAK DITEMUKAN!")
            return

        creds = Credentials.from_service_account_file(path_key, scopes=scope)
        client = gspread.authorize(creds)
        
        # ID Spreadsheet Kak Alif
        spreadsheet_id = "1IGKi2QJL5U6CZ9nBipEXdMF8IJB9QvGgdH1GE3XZdSg"
        sheet = client.open_by_key(spreadsheet_id).get_worksheet(0)
        
        row = [
            str(laporan.tanggal), 
            laporan.ekskul.nama, 
            laporan.ekskul.nama_pembina, 
            laporan.materi, 
            laporan.jumlah_santri, 
            laporan.diinput_pada.strftime("%d/%m/%Y %H:%M"),
            f"Input oleh: {user_obj.username}"
        ]
        sheet.append_row(row)
        print("ALHAMDULILLAH: Data berhasil masuk ke Google Sheets!")
        
    except Exception as e:
        print(f"GAGAL SYNC. Pesan Eror: {e}")

@login_required
def dashboard_admin(request):
    # Logika Admin Alif
    is_alif = (request.user.username == 'alif')
    laporans = LaporanEkskul.objects.all().order_by('-diinput_pada') if is_alif else LaporanEkskul.objects.filter(ekskul__pembina=request.user).order_by('-diinput_pada')
    
    total_p = laporans.count()
    total_s = sum(l.jumlah_santri for l in laporans)
    
    rekap_fee = []
    nama_bulan = ""
    if is_alif:
        today = timezone.now()
        last_m = (today.replace(day=1) - timezone.timedelta(days=1))
        nama_bulan = last_m.strftime("%B %Y")
        for p in Ekskul.objects.all():
            cnt = LaporanEkskul.objects.filter(ekskul=p, tanggal__month=last_m.month, tanggal__year=last_m.year).count()
            if cnt > 0:
                rekap_fee.append({'nama': p.nama_pembina, 'unit': p.nama, 'pertemuan': cnt, 'total': cnt * 55000})

    return render(request, 'dashboard_admin.html', {
        'laporans': laporans, 'is_admin': is_alif, 
        'total_p': total_p, 'total_s': total_s, 'rekap_fee': rekap_fee, 'nama_bulan': nama_bulan
    })

@login_required
def input_laporan(request):
    if request.method == 'POST':
        form = LaporanForm(request.POST, request.FILES)
        if form.is_valid():
            lap = form.save(commit=False)
            if request.user.username != 'alif' and lap.tanggal != timezone.now().date():
                messages.error(request, "Terkunci! Input hanya bisa di hari H.")
                return redirect('dashboard_admin')
            lap.save()
            # JALANKAN SYNC
            sync_to_sheets(lap, request.user)
            messages.success(request, "Laporan Berhasil Disimpan!")
            return redirect('dashboard_admin')
    else:
        form = LaporanForm()
        form.fields['ekskul'].queryset = Ekskul.objects.filter(pembina=request.user)
    return render(request, 'input.html', {'form': form})

# Tetap sertakan fungsi registrasi agar tidak Error lagi
@login_required
def tambah_pembina_dan_ekskul(request):
    if request.user.username != 'alif': return redirect('dashboard_admin')
    if request.method == "POST":
        from django.contrib.auth.forms import UserCreationForm
        f = UserCreationForm(request.POST)
        if f.is_valid():
            u = f.save(); u.set_password(u.username); u.save()
            from .models import Ekskul
            Ekskul.objects.create(nama=request.POST.get('nama_ekskul'), pembina=u, nama_pembina=request.POST.get('nama_lengkap'))
            return redirect('dashboard_admin')
    return render(request, 'tambah_pembina_ekskul.html')

def edit_laporan(request, pk):
    laporan = get_object_or_404(LaporanEkskul, pk=pk)
    if request.method == 'POST':
        form = LaporanForm(request.POST, request.FILES, instance=laporan)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    return render(request, 'input.html', {'form': LaporanForm(instance=laporan), 'edit_mode': True})

def hapus_laporan(request, pk):
    get_object_or_404(LaporanEkskul, pk=pk).delete()
    return redirect('dashboard_admin')
