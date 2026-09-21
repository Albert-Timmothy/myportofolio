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

### Tugas 2

1. Ketika pengguna membuka halaman award, browser mengirim request ke proyek Django. File `portofolio/urls.py` meneruskan request tersebut ke URL aplikasi `main`, lalu `main/urls.py` mencocokkan path `/awards/` dengan view `show_award`. View tersebut mengambil data dari model `Award` melalui `Award.objects.all()`, memasukkannya ke context sebagai `award_list`, lalu mengirim context tersebut ke template `award.html`. Template kemudian menggunakan Django Template Language untuk melakukan perulangan terhadap `award_list` dan menampilkan setiap data award ke browser.

2. Data bagian portofolio baru sebaiknya disimpan pada model karena model membuat data lebih mudah dikelola, diuji, dan dikembangkan. Kalau data award ditulis langsung di template, setiap perubahan isi harus dilakukan dengan mengedit HTML. Dengan model, struktur data tersimpan di database dan template hanya bertanggung jawab untuk menampilkan data. Pendekatan ini membuat aplikasi lebih mudah dipelihara, terutama kalau nanti data ingin ditambah lewat admin, dibuat halaman detail, atau dikembangkan menjadi fitur lain.

3. `makemigrations` digunakan untuk membuat berkas migrasi berdasarkan perubahan pada model, sedangkan `migrate` digunakan untuk menerapkan berkas migrasi tersebut ke database. Contohnya, ketika saya menambahkan model `Award` dengan field `title`, `organizer`, `date`, dan `description`, saya perlu menjalankan `makemigrations` agar Django membuat file migrasi baru. Setelah itu, saya menjalankan `migrate` agar tabel `Award` benar-benar dibuat di database.

## AI Disclosure

Saya menggunakan bantuan AI melalui Claude dengan strategi prompting awal sampai akhir untuk memperhatikan rubrik penilaian, memperhatikan checklist, penalti, dan constraints dari assignment. Saya juga menggunakan AI untuk memberitahu saya salah/error dimana, tetapi konten yang saya masukkan adalah pure saya kerjakan sendiri dengan bantuan AI untuk membantu melihat kesalahan coding yang saya lakukan. Untuk penambahan section tadi saya juga meminta bantuan agar kode tidak mengalami error saat saya memasukkan section awards, experiences, projects.

### Tugas 3

1. Saya pakai `ModelForm` karena field-fieldnya otomatis mengikuti model `Skill` yang sudah saya buat sebelumnya. Jadi saya nggak perlu nulis ulang satu-satu tipe data, batas panjang, atau pilihan kategori di HTML — cukup sekali didefinisikan di model, form-nya otomatis ikut. Ini juga bikin proses validasi dan penyimpanan ke database jadi lebih simpel, saya nggak perlu mikirin dua tempat (HTML dan view) yang bisa saja beda kalau modelnya berubah nanti. Kalau untuk fitur edit, saya tinggal kasih tahu form data mana yang mau diubah, jadi form-nya otomatis terisi nilai lama. Soal `{% csrf_token %}`, itu wajib karena tanpa token itu situs luar bisa saja "menyamar" mengirim data lewat form saya tanpa saya sadari, misalnya menghapus atau menambah skill diam-diam. Jadi token itu semacam tanda pengaman supaya Django yakin form yang dikirim memang benar-benar dari halaman saya sendiri.


2. Menurut saya JSON lebih disukai karena lebih ringkas dan gampang dibaca, baik oleh manusia maupun program. Dibanding XML yang harus pakai tag pembuka-penutup di setiap data, JSON cukup pakai kurung kurawal dan koma, jadi datanya lebih kecil dan lebih cepat dikirim. JSON juga lebih "natural" buat dipakai di JavaScript karena bentuknya mirip banget sama objek/array biasa, tinggal di-parse langsung tanpa proses tambahan yang ribet. XML sebenarnya masih dipakai di beberapa kasus yang butuh struktur sangat ketat atau dokumen kompleks, tapi untuk kebutuhan web modern kayak portofolio saya ini, JSON jauh lebih praktis.

3. Alurnya seperti ini jadinya waktu saya buka halaman skills, aplikasi Django dulu ambil semua data skill dari database, lalu data itu "dibungkus" jadi format JSON supaya bisa dikirim lewat internet. Setelah sampai di sisi tampilan, data JSON itu "dibongkar" lagi jadi objek yang bisa dipakai buat ditampilkan satu-satu di halaman. Proses bungkus-bongkar ini (serialization-deserialization) perlu dilakukan karena data yang tersimpan di database itu bentuknya objek Python yang terikat ke Django, sedangkan yang bisa dikirim lewat internet cuma teks biasa. Jadi harus diubah dulu ke bentuk teks standar (JSON) supaya bisa "dimengerti" siapa pun yang mengaksesnya, baru nanti diubah balik jadi objek supaya bisa ditampilkan lagi di web saya.

## AI Disclosure

Saya menggunakan bantuan AI melalui Claude dengan strategi prompting awal sampai akhir untuk memperhatikan rubrik penilaian, memperhatikan checklist, penalti, dan constraints dari assignment. Saya juga menggunakan AI untuk memberitahu saya salah/error dimana, tetapi konten yang saya masukkan adalah pure saya kerjakan sendiri dengan bantuan AI untuk membantu melihat kesalahan coding yang saya lakukan. Untuk penambahan section tadi saya juga meminta bantuan agar kode tidak mengalami error saat saya memasukkan section awards, experiences, projects.

- **Tools:** Claude (claude.ai).
- **Strategi prompting:** Saya mengunggah berkas soal Individual Assignment 3 (checklist, rubrik, dan pertanyaan reflektif), lalu meminta Claude memahami  dan membuat section Skills & Tools yang sesuai dengan ketentuan tersebut. Saya mengerjakannya bertahap: memahami struktur kode, menambahkan link Project di navbar, lalu membuat fitur Skills & Tools.

