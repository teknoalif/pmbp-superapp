from django.shortcuts import render, redirect
from .models import Ekskul, LaporanEkskul
from django.contrib.auth.decorators import login_required
import gspread
from google.oauth2.service_account import Credentials
import os

# Fungsi yang dicari oleh urls.py
@login_required
def dashboard_admin(request):
    laporan_list = LaporanEkskul.objects.all().order_by('-diinput_pada')
    return render(request, 'dashboard_admin.html', {'laporan_list': laporan_list})

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
        # Fungsi sinkronisasi (opsional, pastikan sudah didefinisikan jika dipakai)
        # sync_to_sheets(laporan, request) 
        return redirect('dashboard_admin')
    
    ekskuls = Ekskul.objects.filter(pembina=request.user)
    return render(request, 'input.html', {'ekskuls': ekskuls})