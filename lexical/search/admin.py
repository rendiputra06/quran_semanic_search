from django.contrib import admin
from .models import Ayat, Surah

admin.site.site_header = 'Pencarian Al-Quran'
admin.site.site_title = 'Pencarian Al-Quran'

@admin.register(Ayat)
class ModelAyat(admin.ModelAdmin):
    list_display = ['__str__', 'nomor_ayat', 'surah_id', 'nomor_di_alquran', 'halaman', 'kuarterHizb', 'juz', 'sajda']
    list_filter = ['surah_id', 'juz', 'kuarterHizb', 'halaman', 'sajda']
    search_fields = ['isi_ayat', 'isi_ayat_tanpa_tashkeel', 'ayat_indo']

@admin.register(Surah)
class ModelSurah(admin.ModelAdmin):
    list_display = ['nama', 'nama_tanpa_tashkeel', 'nama_latin']
    search_fields = ['nama', 'nama_tanpa_tashkeel', 'nama_latin']

