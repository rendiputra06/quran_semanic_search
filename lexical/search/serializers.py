from rest_framework import serializers
from .models import Ayat, Surah

class AyatSerializer(serializers.ModelSerializer):
    surah = serializers.StringRelatedField()

    class Meta:
        model = Ayat
        fields = [
            'nomor_ayat',
            'halaman',
            'kuarterHizb',
            'juz',
            'surah',
            'isi_ayat',
            'isi_ayat_tanpa_tashkeel',
            'nomor_di_surah',
            'nomor_di_alquran',
            'sajda',
            'ayat_indo',
        ]
    def get_surah_details(self, obj):
        # Assuming 'surah' is a ForeignKey in Ayat model
        surah = obj.surah_id
        return {
            'surah_name': surah.nama,
            'surah_latin_name': surah.nama_latin,
            'surah_without_tashkeel': surah.nama_tanpa_tashkeel
            # Add other fields you want from Surah
        }

class SurahSerializer(serializers.ModelSerializer):

    class Meta:
        model = Surah
        fields = ['nama','nama_latin', 'nama_tanpa_tashkeel']
