from django import forms
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
