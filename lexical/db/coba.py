import sqlite3
import json

# Menghubungkan ke database Quran lama
quran_db = sqlite3.connect('../db.sqlite3')
quran_cr = quran_db.cursor()

# Menjalankan query SQL
quran_cr.execute('SELECT * FROM search_surah')

# Mengambil semua data
data = quran_cr.fetchall()

# Menutup koneksi
quran_db.close()


# Menampilkan data
for row in data:
    print(row[0])
    # Membaca file JSON di luar loop
    with open(f'./surah/{row[0]}.json', 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    
    django_db = sqlite3.connect('../db2.sqlite3')
    cr = django_db.cursor()
    cr.execute(
        '''INSERT INTO search_surah
        (nama, nama_latin, nama_tanpa_tashkeel) 
        VALUES (?, ?, ?)''',
        (row[1], data_json[str(row[0])]['name_latin'], row[2])
    )


    django_db.commit()
    print(data_json[str(row[0])]['name_latin'])  # Menampilkan kunci dari data JSON

