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
3. Terapkan migrasi database:
   ```bash
   python manage.py migrate
   ```
4. Jalankan server:
   ```bash
   python manage.py runserver
   ```
5. Buka website di local `http://127.0.0.1:8000/`.

### Tugas 1

1. Iya betul, saya menggunakan beberapa elemen semantik HTML5 sebagai berikut `<section>`, `<article>`, `<header>`, `<main>`, dan `<footer>`. Elemen-elemen tersebut bakal membantu membagi halaman menjadi bagian-bagian yang sudah saya susun dengan jelas, misalnya profile saya, awards yang saya dapatkan, experience yang pernah saya lalui, projects yang pernah saya kerjakan, dan skills yang saya gunakan serta dapatkan. Dengan struktur seperti ini saya merasa akan membuat isi halaman lebih mudah dibaca, lebih mudah diberi style melalui CSS, dan lebih siap dikembangkan pada tugas berikutnya.

2. Menurut refleksif saya, tantangan utama saat membuat tugas individual assignment 1 yaitu, tampilan responsif adalah menjaga agar layout dua kolom, foto profil, timeline, dan project foto tetap rapi di layar kecil jadi harus bolak balik nyesuain. Kalau buat tampilan desktop,saya ngeliatnya grid cocok aja karena dia luas. Tapi kalau untuk tampilan mobile, elemennya mau gamau  perlu disusun satu kolom agar teks dan gambar tidak terlalu sempit gitu. Jadi akhirnya, saya mengevaluasi bahwa elemen yang perlu berubah itu adalah posisi berdasarkan prioritas informasi yang mau saya sampaikan seperti, identitas dan foto tetap muncul dulu, lalu detail pendukung seperti pengalaman, penghargaan, proyek, dan skills.

3. Okay karena website ini masih static web murni, semua informasi harus ditulis itu langsung saya coding/ketik di HTML. Batasannya yang sudah pasti lawannya dari statis adalah konten belum bisa dikelola secara dinamis, belum ada database tetapi next mungkin bakal dipelajari, dan juga belum ada fitur interaksi seperti filtering project atau form kontak ya fitur-fitur yang sering kita lihat kalau buka web portofolio sepuh diluar sana. Pada assignment berikutnya, saya ingin menambahkan data project dan experience melalui model Django agar konten portofolio bisa diperbarui dari database tanpa mengubah HTML secara manual.

## AI Disclosure

Saya menggunakan bantuan AI melalui Claude dengan strategi prompting awal sampai akhir untuk memperhatikan rubrik penilaian, memperhatikan checklist, penalti, dan constraints dari assignment. Saya juga menggunakan AI untuk memberitahu saya salah/error dimana, tetapi konten yang saya masukkan adalah pure saya kerjakan sendiri dengan bantuan AI untuk membantu melihat kesalahan coding yang saya lakukan. Untuk penambahan section tadi saya juga meminta bantuan agar kode tidak mengalami error saat saya memasukkan section awards, experiences, projects.

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

## Tugas 4

#### Ringkasan Fitur
 
Tugas 4 menambahkan autentikasi, otorisasi berbasis peran, dan fitur star pada bagian **Projects** dan **Skills & Tools**. Halaman daftar tetap bisa dibaca siapa pun, sedangkan tindakan yang mengubah data mengikuti hak akses pengguna.
 
| Peran | Baca data | Star | Tambah | Ubah | Hapus |
|---|---|---|---|---|---|
| Pengunjung tanpa login | Ya | Tidak (diarahkan ke login) | Tidak | Tidak | Tidak |
| Pengguna biasa | Ya | Ya | Tidak | Tidak | Tidak |
| Editor | Ya | Ya | Tidak | Ya | Tidak |
| Pemilik portofolio (superuser) | Ya | Ya | Ya | Ya | Ya |

#### Implementasi
 
**Autentikasi dan otorisasi (server-side)**
- Semua view yang mengubah data memakai `@login_required`, sehingga pengunjung tanpa login diarahkan ke halaman login.
- Setelah login, hak akses dicek dengan `request.user.has_perm(...)` dan mengembalikan HTTP 403 (`PermissionDenied`) bila tidak berhak. Permission yang dipakai: `add`, `change`, dan `delete` untuk model `Project` dan `Skill`.
- Superuser otomatis lolos semua pengecekan permission, sedangkan Editor hanya memiliki permission `change`.
- View hapus dan view star hanya menerima method POST (`@require_POST`).
**Tampilan (template)**
- Tombol Tambah, Edit, dan Hapus disembunyikan dengan `{% if perms.main.<aksi>_<model> %}`, sehingga tampilan selalu konsisten dengan pengecekan di server.
- Pengunjung tanpa login melihat tombol Star berupa tautan ke halaman login.
**Fitur Star**
- Model `Project` dan `Skill` memiliki `starred_by = ManyToManyField(User)`, sehingga satu pengguna hanya bisa memberi satu star per item.
- View `toggle_star` (Project) dan `toggle_skill_star` (Skill) memberi atau membatalkan star melalui POST dengan `{% csrf_token %}`. Halaman menampilkan jumlah total star dan status star pengguna yang sedang login (Star atau Unstar).
**Keamanan API**
- Endpoint `/api/projects/` dan `/api/skills/` membatasi field yang diserialisasi dan tidak menyertakan `starred_by`, sehingga identitas pengguna yang memberi star tidak terbuka ke publik.
- Daftar username pemberi star juga dihapus dari tampilan halaman.
**Pengujian manual**
 
Fitur diuji dengan empat peran (anonim, pengguna biasa, editor, superuser) pada halaman dan URL langsung untuk create, update, delete, dan star. Hasilnya: anonim diarahkan ke login, pengguna biasa dan editor mendapat 403 untuk aksi yang tidak diizinkan, tombol yang tidak berhak tidak tampil, dan `python manage.py runserver` berjalan tanpa error.

**Reflektif**
Dari sini saya belajar bahwa autentikasi hanya menjawab "siapa kamu", sedangkan otorisasi menjawab "kamu boleh apa". Cek `is_superuser` ternyata tidak cukup karena Editor ikut terblokir, jadi lebih tepat memakai `has_perm`. Menyembunyikan tombol di template juga hanya soal tampilan, yang benar-benar mengamankan adalah cek di server. Saya juga baru sadar kalau JSON bisa membocorkan username lewat relasi `starred_by`, dan itu saya buktikan sendiri dengan membuka `/api/projects/`.
 
## AI Disclosure
Saya menggunakan Claude (claude.ai) untuk memandu pengerjaan Tugas 4. Saya mengunggah soal dan ZIP proyek, lalu meminta dibimbing bertahap dari awal, tidak langsung diberi jawaban. Mulai dari membuat grup Editor di Django Admin, memproteksi view Project dan Skills, menyembunyikan tombol di template, sampai merapikan `toggle_star` dan JSON. Saya sendiri yang menjalankan server, membuat akun uji, migrasi, dan menguji empat peran di browser. Fitur star pada Skills adalah keputusan saya sebagai fitur tambahan.

### Tugas 5
 
1. *Debouncing* adalah teknik menunda eksekusi sebuah fungsi sampai pengguna berhenti melakukan aksi selama waktu tertentu. Pada pencarian, setiap ketikan akan mereset timer, dan permintaan baru hanya dikirim bila tidak ada ketikan baru selama jeda tersebut (di proyek ini 300 ms). Teknik ini penting pada pencarian AJAX karena tanpa debouncing, mengetik kata "django" bisa mengirim enam permintaan ke server, padahal hanya hasil akhir yang dibutuhkan. Akibatnya beban server dan database meningkat, jaringan terpakai sia-sia, dan hasil bisa tampil tidak berurutan karena respons lama datang belakangan. Dengan debouncing, jumlah permintaan berkurang drastis dan antarmuka terasa lebih mulus.

2. `await` membuat fungsi `async` berhenti sementara pada baris tersebut sampai `Promise` dari `fetch()` selesai, lalu mengembalikan nilai hasilnya (objek `Response`). Karena itu, kode setelahnya dapat langsung memakai `response` seperti kode biasa. Jika `await` tidak dipakai, `fetch()` hanya mengembalikan `Promise` yang belum selesai dan eksekusi langsung lanjut ke baris berikutnya. Akibatnya `response.ok` atau `response.json()` dipanggil pada `Promise`, bukan pada respons asli, sehingga datanya `undefined` atau muncul error, dan kondisi loading bisa langsung hilang sebelum data benar-benar tiba. Selain itu, `try/catch` juga tidak akan menangkap error jaringan karena error terjadi setelah blok `try` selesai.

3. XSS (*Cross-Site Scripting*) adalah serangan ketika penyerang menyisipkan skrip berbahaya (misalnya lewat input yang berisi `<img src="x" onerror="...">`) yang kemudian dieksekusi di browser pengguna lain, sehingga bisa mencuri cookie sesi atau melakukan aksi atas nama korban. Data dari AJAX lebih rentan karena template Django melakukan *auto-escaping* secara otomatis pada `{{ variabel }}`, sedangkan saat memakai JavaScript, kita sendiri yang menyisipkan data ke DOM. Jika memakai `innerHTML` atau *template literal* tanpa escaping, string dari JSON akan dibaca sebagai HTML aktif. Perlindungan tidak lagi otomatis, jadi harus dilakukan manual lewat `textContent` atau `escapeHtml`, ditambah pembersihan di server dengan `strip_tags`.

## AI Disclosure
 
Saya menggunakan Claude (claude.ai) untuk memandu pengerjaan Tugas 5. Saya mengunggah soal dan ZIP proyek, lalu meminta dibimbing bertahap dari Tutorial 05 (AJAX, debounce, modal, toast, XSS) sampai menerapkannya pada section Skills & Tools, tidak langsung diberi jawaban. Saya sendiri yang menjalankan server, menguji keempat peran di browser, mencoba payload XSS, dan melakukan commit secara bertahap. Claude juga dipakai untuk memeriksa kode terhadap checklist dan rubrik sebelum dikumpulkan, serta membantu menyusun draf README ini, yang kemudian saya baca dan sesuaikan dengan pemahaman saya. Keterbatasan AI yang saya temui: pengecekan kode oleh AI hanya terbatas pada berkas yang saya unggah, sehingga hasil akhir tetap harus saya verifikasi sendiri lewat pengujian di browser.

### Tugas 6

1. Menurut saya, REST (*Representational State Transfer*) adalah gaya arsitektur untuk mengatur komunikasi client dan server berdasarkan resource, misalnya skill pada `/api/v1/skills/<uuid>/`. Jadi mengembalikan JSON saja belum cukup untuk menyebut API RESTful, karena JSON hanya format datanya. API juga perlu punya antarmuka yang konsisten, memakai method dan status HTTP sesuai maknanya, serta memperhatikan prinsip seperti pemisahan client-server, stateless, caching, dan sistem berlapis. Stateless berarti setiap request membawa informasi yang diperlukan untuk dipahami tanpa bergantung pada urutan request sebelumnya. Di tugas ini saya menerapkan pola resource dan method HTTP, tetapi autentikasinya masih menggunakan sesi Django, sehingga saya tidak mengklaim semua prinsip REST sudah dipenuhi secara ketat. Perbedaan PUT dan PATCH ada pada cakupan pembaruannya: PUT digunakan untuk mengirim representasi pengganti resource, sedangkan PATCH hanya mengubah sebagian field. Contohnya, PUT cocok saat mengirim ulang seluruh data skill dari formulir lengkap, sementara PATCH cocok saat hanya mengganti `proficiency` dari 3 menjadi 4. Halaman edit saya memakai PATCH. Pada DRF, PATCH diproses dengan `partial=True`, jadi field wajib yang tidak dikirim tidak langsung dianggap error. PUT tetap memvalidasi field wajib, tetapi perilaku field opsional yang tidak dikirim juga bergantung pada serializer, bukan otomatis selalu dikosongkan.

2. Serializer pada DRF membantu mengubah objek model menjadi data yang bisa dirender sebagai JSON, sekaligus memvalidasi data yang masuk sebelum disimpan ke database. Di bagian Skills & Tools, saya memakai `SkillSerializer` dengan daftar field yang ditulis satu-satu agar jelas data apa saja yang boleh keluar. Nama dan deskripsi dibersihkan dengan `strip_tags`, lalu nama yang kosong setelah dibersihkan ditolak. Field `star_count`, `is_starred`, dan `starred_by_names` dihitung dari relasi star dan bersifat read-only, jadi pengguna tidak bisa memalsukan jumlah atau identitas pemberi star lewat payload. Dibanding merakit dictionary manual dengan `JsonResponse`, serializer membuat aturan representasi dan validasi terkumpul di satu tempat. Saya juga bisa memakai serializer yang sama untuk daftar, detail, tambah, dan edit, dengan pesan kesalahan per field yang lebih konsisten. `JsonResponse` sendiri hanya mengirim respons JSON, sehingga validasi dan penyimpanan tetap harus saya tulis terpisah.

3. Autentikasi menjawab siapa pengguna yang sedang mengirim request, sedangkan otorisasi menjawab tindakan apa yang boleh dilakukan pengguna itu. Pada API ini, `SessionAuthentication` mengenali pengguna dari sesi login Django. Setelah itu, `IsPortfolioOwnerOrEditorOrReadOnly` memeriksa hak akses: semua orang boleh membaca, pengguna biasa boleh star melalui endpoint tersendiri, Editor dengan permission `main.change_skill` boleh PUT/PATCH, dan superuser boleh membuat serta menghapus data. Endpoint star memakai `IsAuthenticated` dan mengambil akun dari `request.user`, bukan dari ID pengguna yang dikirim client. Menyembunyikan tombol hanya membantu tampilan, karena request tetap bisa dikirim langsung lewat alat HTTP atau JavaScript. Karena itu, pengecekan harus dilakukan di server. View tambah dan hapus lama juga saya sesuaikan agar pengguna non-superuser yang kebetulan memiliki permission tambahan tidak bisa melewati aturan API lewat URL lama.

4. Token CSRF tetap diperlukan karena browser otomatis menyertakan cookie sesi pada request yang memenuhi aturan cookie. Situs lain bisa mencoba memanfaatkan sesi login tersebut untuk mengirim tindakan atas nama pengguna. Mengirim JSON tidak dengan sendirinya menggantikan perlindungan CSRF. Dengan `SessionAuthentication`, request yang mengubah data dari pengguna yang sudah login harus lolos pemeriksaan token CSRF. Template saya menyediakan `{% csrf_token %}`, kemudian JavaScript mengirim nilainya melalui header `X-CSRFToken` saat POST, PATCH, dan DELETE. Tes dengan `force_authenticate` memaksa identitas pengguna untuk menguji permission, sehingga tidak membuktikan bahwa alur autentikasi sesi dan pemeriksaan CSRF benar-benar berjalan. Karena itu, tes tambahan memakai `APIClient(enforce_csrf_checks=True)` dan `.login()`: request tanpa token harus mendapat 403 dan database tidak berubah, sedangkan request dengan token yang sesuai boleh berhasil. Pemeriksaan ini juga mencakup edit oleh Editor/pemilik serta star oleh pengguna biasa, Editor, dan pemilik.


## AI Disclosure
Saya menggunakan Claude (claude.ai) untuk memandu pengerjaan Tugas 6. Saya mengunggah soal dan ZIP proyek, lalu meminta dibimbing bertahap dari Tutorial. Saya sendiri yang menjalankan server, menguji keempat peran di browser dan melakukan commit secara bertahap. Claude juga dipakai untuk memeriksa kode terhadap checklist dan rubrik sebelum dikumpulkan. Keterbatasan AI yang saya temui: pengecekan kode oleh AI hanya terbatas pada berkas yang saya unggah, sehingga hasil akhir tetap harus saya verifikasi sendiri lewat pengujian di 
