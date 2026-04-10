from django.shortcuts import render, redirect
from .models import Ekskul, LaporanEkskul
from django.contrib.auth.decorators import login_required
import gspread
from google.oauth2.service_account import Credentials
import os

# Fungsi Dashboard untuk Admin/Staf
@login_required
def dashboard_admin(request):
    laporan_list = LaporanEkskul.objects.all().order_by('-diinput_pada')
    return render(request, 'dashboard_admin.html', {'laporan_list': laporan_list})

# Fungsi Input Laporan untuk Asatiz
@login_required
def input_laporan(request):
    if request.method == 'POST':
        ekskul_id = request.POST.get('ekskul')
        ekskul_obj = Ekskul.objects.get(id=ekskul_id)
        
        laporan = LaporanEkskul.objects.create(
            ekskul=ekskul_obj,
            materi=request.POST.get('materi'),
            jumlah_santri=request.POST.get('jumlah_santri'),
            foto=request.FILES.get('foto')
        )
        
        # Jalankan sinkronisasi Sheets jika file kunci ada
        try:
            sync_to_sheets(laporan, request)
        except:
            pass
            
        return redirect('dashboard_admin')
    
    ekskuls = Ekskul.objects.filter(pembina=request.user)
    return render(request, 'input.html', {'ekskuls': ekskuls})

def sync_to_sheets(laporan, request):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_key = os.path.join(base_dir, "google_key.json")
    if os.path.exists(path_key):
        creds = Credentials.from_service_account_file(path_key, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1IGKi2QJL5U6CZ9nBipEXdMF8IJB9QvGgdH1GE3XZdSg").get_worksheet(0)
        
        foto_url = request.build_absolute_uri(laporan.foto.url) if laporan.foto else ""
        row = [str(laporan.tanggal), laporan.ekskul.nama, laporan.ekskul.nama_pembina, laporan.materi, laporan.jumlah_santri, foto_url]
        sheet.append_row(row)