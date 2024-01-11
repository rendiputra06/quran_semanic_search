from .models import Ayat
from .serializers import AyatSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.shortcuts import get_object_or_404, render


@api_view(['GET'])
def get_all(request) -> None:
    """
        Returns all verses in Database.
        Not really effective for search, so use it to clone the database or such on.
    """
    verses = Ayat.objects.all()
    data = AyatSerializer(verses, many=True).data
    return Response({'length': len(data), 'data': data})



@api_view(['GET'])
def search(request, words) -> str:
    """
        Search in verses using insensitive contains.
        Return all verses with given words.
    """
    verses = Ayat.objects.filter(
        Q(isi_ayat__icontains=words) | Q(isi_ayat_tanpa_tashkeel__icontains=words)
    )
    data = AyatSerializer(verses, many=True).data
    return Response({'length': len(data), 'data': data})


@api_view(['GET'])
def get_surah(request, surah_id) -> int:
    """
        Retrieving surah_pk, searching in database with verse_pk:
        verse_pk: S***V*** | surah_pk -> first part of verse_pk (S***).
        Returns all Verses of a Surah.
    """
    surah_pk = f"S{str(surah_id).zfill(3)}"
    verse_id = Ayat.objects.filter(nomor_ayat__icontains=surah_pk)
    data = AyatSerializer(verse_id, many=True).data
    return Response({'length': len(data), 'data': data})


@api_view(['GET'])
def get_verse_in_surah(request, surah_id, verse_id) -> int:
    """
        Taking two integers and convert them to verse_pk,
        to search in database with it using get_object_or_404.
        Returns the Verse.
    """
    verse_pk = f'S{str(surah_id).zfill(3)}V{str(verse_id).zfill(3)}'
    verse = get_object_or_404(Ayat, nomor_ayat=verse_pk)
    data = AyatSerializer(verse).data
    return Response({'data': data})


@api_view(['GET'])
def get_verse_in_quran(request, verse_id) -> int:
    """
        Taking verse_id of all Quran, 
        to search in database with it using get_object_or_404.
        Returns the Verse.
    """
    verse = get_object_or_404(Ayat, nomor_di_alquran=verse_id)
    data = AyatSerializer(verse).data
    return Response({'data': data})

@api_view(['GET'])
def cari(request, words) -> str:
    """
        Search in verses using insensitive contains.
        Return all verses with given words.
    """
    verses = Ayat.objects.filter(
        Q(isi_ayat__icontains=words) | Q(isi_ayat_tanpa_tashkeel__icontains=words) | Q(ayat_indo__icontains=words)
    )
    data = AyatSerializer(verses, many=True).data
    return Response({'length': len(data), 'data': data})

def api_docs(request):
    return render(request, 'search/api.html')
