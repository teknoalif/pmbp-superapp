from django.shortcuts import render, redirect
from .models import Ekskul, LaporanEkskul
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import gspread
from google.oauth2.service_account import Credentials
import os

def sync_to_sheets(laporan, request):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_key = os.path.join(base_dir, "google_key.json")
        
        creds = Credentials.from_service_account_file(path_key, scopes=scope)
        client = gspread.authorize(creds)
        # ID Spreadsheet Kak Alif
        spreadsheet_id = "1IGKi2QJL5U6CZ9nBipEXdMF8IJB9QvGgdH1GE3XZdSg"
        sheet = client.open_by_key(spreadsheet_id).get_worksheet(0)
        
        # Ambil URL foto secara absolut (biar bisa diklik dari mana saja)
        foto_url = ""
        if laporan.foto:
            foto_url = request.build_absolute_uri(laporan.foto.url)
        
        row = [
            str(laporan.tanggal), 
            laporan.ekskul.nama, 
            laporan.ekskul.nama_pembina, 
            laporan.materi, 
            laporan.jumlah_santri, 
            foto_url  # Masuk ke kolom terakhir
        ]
        sheet.append_row(row)
    except Exception as e:
        print(f"Eror Sinkronisasi: {e}")

@login_required
def input_laporan(request):
    if request.method == 'POST':
        # Pastikan request.FILES ikut diproses
        ekskul_id = request.POST.get('ekskul')
        ekskul_obj = Ekskul.objects.get(id=ekskul_id)
        
        laporan = LaporanEkskul.objects.create(
            ekskul=ekskul_obj,
            materi=request.POST.get('materi'),
            jumlah_santri=request.POST.get('jumlah_santri'),
            foto=request.FILES.get('foto')
        )
        
        # Jalankan sinkronisasi
        sync_to_sheets(laporan, request)
        
        messages.success(request, "Laporan & Foto Berhasil Terkirim!")
        return redirect('dashboard_admin')
    
    ekskuls = Ekskul.objects.filter(pembina=request.user)
    return render(request, 'input.html', {'ekskuls': ekskuls})