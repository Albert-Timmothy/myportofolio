# Portofolio Pemrograman Berbasis Platform (PBP)

Nama : Albert Timmothy Ariajaya

NPM : 2506656381

Kelas : Kelas F

## Deskripsi Proyek

Saya membuat Website portofolio pribadi dengan Django untuk mata kuliah Pemrograman Berbasis Platform. Proyek ini intinya akan menampilkan profil singkat, awards, experiences, proyek, dan kemampuan menggunakan Django sebagai server dasar dengan halaman statis HTML5 dan CSS3.

## Cara Menjalankan

1. Aktifkan virtual environment:
   ```bash
   env\Scripts\activate
   ```
2. Install dependency jika belum tersedia:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan server:
   ```bash
   python manage.py runserver
   ```
4. Buka website di local`http://127.0.0.1:8000/`.

### Tugas 1

1. Iya betul, saya menggunakan beberapa elemen semantik HTML5 sebagai berikut `<section>`, `<article>`, `<header>`, `<main>`, dan `<footer>`. Elemen-elemen tersebut bakal membantu membagi halaman menjadi bagian-bagian yang sudah saya susun dengan jelas, misalnya profile saya, awards yang saya dapatkan, experience yang pernah saya lalui, projects yang pernah saya kerjakan, dan skills yang saya gunakan serta dapatkan. Dengan struktur seperti ini saya merasa akan membuat isi halaman lebih mudah dibaca, lebih mudah diberi style melalui CSS, dan lebih siap dikembangkan pada tugas berikutnya.

2. Menurut refleksif saya, tantangan utama saat membuat tugas individual assignment 1 yaitu, tampilan responsif adalah menjaga agar layout dua kolom, foto profil, timeline, dan project foto tetap rapi di layar kecil jadi harus bolak balik nyesuain. Kalau buat tampilan desktop,saya ngeliatnya grid cocok aja karena dia luas. Tapi kalau untuk tampilan mobile, elemennya mau gamau  perlu disusun satu kolom agar teks dan gambar tidak terlalu sempit gitu. Jadi akhirnya, saya mengevaluasi bahwa elemen yang perlu berubah itu adalah posisi berdasarkan prioritas informasi yang mau saya sampaikan seperti, identitas dan foto tetap muncul dulu, lalu detail pendukung seperti pengalaman, penghargaan, proyek, dan skills.

3. Okay karena website ini masih static web murni, semua informasi harus ditulis itu langsung saya coding/ketik di HTML. Batasannya yang sudah pasti lawannya dari statis adalah konten belum bisa dikelola secara dinamis, belum ada database tetapi next mungkin bakal dipelajari, dan juga belum ada fitur interaksi seperti filtering project atau form kontak ya fitur-fitur yang sering kita lihat kalau buka web portofolio sepuh diluar sana. Pada assignment berikutnya, saya ingin menambahkan data project dan experience melalui model Django agar konten portofolio bisa diperbarui dari database tanpa mengubah HTML secara manual.

