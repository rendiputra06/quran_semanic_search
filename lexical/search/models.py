from django.db import models

# Membuat model-model di sini

class Ayat(models.Model):
    nomor_ayat = models.CharField(max_length=8, null=False, blank=False, unique=True, verbose_name='Nomor Ayat')
    halaman = models.PositiveIntegerField(null=False, blank=False, verbose_name='Halaman')
    kuarterHizb = models.PositiveIntegerField(null=False, blank=False, verbose_name='Kuarter Hizb')
    juz = models.PositiveIntegerField(null=False, blank=False, verbose_name='Juz')
    surah = models.ForeignKey('Surah', on_delete=models.CASCADE, null=True, blank=True, related_name='surah',
                              verbose_name='Surah')
    isi_ayat = models.CharField(max_length=5000, null=False, blank=False, verbose_name='Isi Ayat')
    isi_ayat_tanpa_tashkeel = models.CharField(max_length=1000, null=False, blank=False, verbose_name='Isi Ayat tanpa Tashkeel')
    ayat_indo = models.CharField(max_length=5000, null=False, blank=False, verbose_name='Isi Ayat Bahasa Indonesia')
    nomor_di_surah = models.PositiveIntegerField(null=False, blank=False, verbose_name='Nomor Ayat di Surah')
    nomor_di_alquran = models.PositiveIntegerField(null=False, blank=False, unique=True,
                                                   verbose_name='Nomor Ayat di Al-Quran')
    sajda = models.BooleanField(verbose_name='Apakah Ayat Ini Mengandung Sujud')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ayat'
        verbose_name_plural = 'Ayat'

    def __str__(self):
        return self.isi_ayat[:50]


class Surah(models.Model):
    nama = models.CharField(max_length=50, verbose_name="Nama Surah")
    nama_latin = models.CharField(max_length=50, verbose_name="Nama Surah Latin")
    nama_tanpa_tashkeel = models.CharField(max_length=30, verbose_name="Nama Surah tanpa Tashkeel")

    class Meta:
        ordering = ['id']
        verbose_name = 'Surah'
        verbose_name_plural = 'Surah'

    def __str__(self):
        return self.nama
