# Checklist dan pengerjaan Tugas 6

Bagian tugas mandiri: **Skills & Tools**, memakai model `Skill` yang sudah ada. Projects tetap menjadi implementasi Tutorial 07. Checklist ini mencatat kode dan pemeriksaan lokal, bukan bukti pengumpulan di SCELE.

## Tahapan implementasi

1. Serializer, permission, API, dan integrasi daftar/tambah/hapus/star sudah tersedia pada commit sebelumnya. `SkillSerializer` menggunakan field eksplisit, membersihkan teks lewat `strip_tags`, serta menyediakan `star_count`, `is_starred`, dan `starred_by_names` yang read-only. Username menjadi atribusi star; email dan password tidak disertakan.
2. Melengkapi halaman edit dengan `fetch()` PATCH, CSRF, toast, dan pembaruan nilai form dari hasil validasi server. View tambah/hapus lama dibatasi ke superuser agar tidak menjadi jalan melewati aturan API.
3. Memperkuat tes penolakan dengan pemeriksaan database, pengujian sesi Editor/pemilik untuk edit, dan CSRF star untuk ketiga peran yang login.
4. Menulis jawaban reflektif dan AI disclosure pada bagian `### Tugas 6` di README.

## Checklist kode

- [x] `ModelSerializer` dengan daftar field eksplisit di `main/serializers.py`.
- [x] Informasi jumlah/status star read-only; tidak menampilkan email atau password hash.
- [x] Validasi nama dan deskripsi melalui `validate_<field>` serta `strip_tags`.
- [x] `IsPortfolioOwnerOrEditorOrReadOnly` pada daftar/detail; Editor menggunakan `main.change_skill`, mengikuti Tugas 4.
- [x] `IsAuthenticated` pada star; identitas pemberi star berasal dari `request.user`.
- [x] Function-based API dengan `@api_view` dan `SessionAuthentication`.
- [x] Pencarian `?name=...` dan filter tambahan `&category=...` pada endpoint daftar.
- [x] Respons 201, 400, 403, 404, dan 204 sesuai hasil operasi.
- [x] URL unik pada `/api/v1/skills/` dengan converter UUID sesuai primary key.
- [x] Daftar, pencarian, tambah, hapus, dan star menggunakan API tanpa reload.
- [x] Halaman edit memakai PATCH; dapat diakses Editor dan superuser.
- [x] Pesan API 400/403 ditampilkan lewat toast; teks memakai `textContent` atau properti `value`.
- [x] Setiap operasi fetch yang mengubah data mengirim `X-CSRFToken`.
- [x] Template menyediakan `{% csrf_token %}` termasuk untuk pengguna biasa dan Editor.
- [x] View lama untuk tambah/hapus mengikuti pembatasan superuser.
- [x] `APITestCase` mencakup empat peran, validasi, star, dan pemeriksaan database pada penolakan.
- [x] Tes CSRF memakai `APIClient(enforce_csrf_checks=True)` dan `.login()`.

## Endpoint

| Endpoint | Method | Hak akses |
|---|---|---|
| `/api/v1/skills/` | GET | Semua pengguna |
| `/api/v1/skills/` | POST | Superuser |
| `/api/v1/skills/<uuid>/` | GET | Semua pengguna |
| `/api/v1/skills/<uuid>/` | PUT, PATCH | Editor dengan `change_skill` dan superuser |
| `/api/v1/skills/<uuid>/` | DELETE | Superuser |
| `/api/v1/skills/<uuid>/star/` | POST | Semua pengguna yang login |

## Menjalankan dan memeriksa

```powershell
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py test main
python manage.py runserver
```

`createsuperuser` hanya perlu dilakukan jika akun pemilik belum tersedia. Di Django Admin, buat grup `Editor`, berikan permission `main | skill | Can change skill`, lalu masukkan akun uji ke grup itu. Nama grup saja tidak memberikan permission. Untuk tes otomatis, akun dan grup dibuat sendiri di database pengujian.

Buka `/skills/`, `/api/v1/skills/` (Browsable API), dan `/projects/`. Uji di browser dengan akun anonim, pengguna biasa, Editor, dan superuser. Saat edit, periksa Network: request harus PATCH ke `/api/v1/skills/<uuid>/`, bukan POST form ke halaman edit. Data tetap tersimpan setelah membuka kembali daftar. Coba nama kosong, cabut permission pada sesi aktif untuk memeriksa toast 403, dan pastikan star serta pencarian tidak me-reload halaman.

Pemeriksaan otomatis bukan pengganti pemeriksaan visual browser. Jangan menganggap petunjuk manual di atas sebagai laporan bahwa semua interaksi browser sudah dilakukan.

Hasil pemeriksaan lokal pada 9 November 2026:

- `python manage.py test main`: **66 tes lulus**, termasuk tes Projects Tutorial 07.
- `python manage.py makemigrations --check --dry-run`: tidak ada perubahan model yang memerlukan migrasi.
- `python manage.py runserver 127.0.0.1:8765 --noreload`: berhasil melayani `/skills/`, `/projects/`, `/api/v1/skills/`, dan `/api/v1/projects/` dengan HTTP 200; endpoint API diminta dengan `Accept: text/html` untuk memeriksa Browsable API.
- `git diff --check`: tidak ada kesalahan whitespace.
- Pemeriksaan visual/interaksi browser belum dilakukan. `node --check` belum berhasil dijalankan karena Node tidak tersedia pada lingkungan ini.
- Django mengeluarkan peringatan folder `staticfiles` belum tersedia saat tes; ini tidak menggagalkan tes. Untuk deployment, jalankan `python manage.py collectstatic --noinput` sesuai konfigurasi hosting.

## Log bantuan AI

- Tool: Codex pada percakapan pengerjaan ini.
- Prompt pengguna: meminta pemeriksaan seluruh checklist dan syarat PDF, pengerjaan bertahap, README mengikuti tugas sebelumnya, serta perintah commit/push berbahasa Indonesia dengan reflektif di tahap terakhir.
- Tindakan: membaca PDF dan kode lama; menemukan edit belum melalui API dan izin view lama lebih luas; menambahkan PATCH, menyelaraskan izin, menambah tes, dan menyusun dokumentasi.
- Batasan: AI tidak dapat membuktikan pengumpulan Tutorial 07 di SCELE atau pengalaman belajar pribadi pengguna. Pemeriksaan browser dan refleksi pribadi tetap perlu ditinjau pengguna. Log ini adalah ringkasan prompting, bukan transkrip lengkap.

## Pengumpulan yang perlu dilakukan sendiri

- [ ] Pastikan Tutorial 07 sudah diselesaikan paling lambat **4 November 2026, 23.59 WIB** (prasyarat penilaian).
- [ ] Tinjau jawaban reflektif dan AI disclosure agar sesuai pemahaman serta tindakan pribadi.
- [ ] Jalankan pemeriksaan manual browser di atas.
- [ ] Commit bertahap dan push ke GitHub sebelum **9 November 2026, 23.59 WIB**.
- [ ] Pastikan repository GitHub publik.
- [ ] Kirim **tautan commit akhir**, bukan hanya tautan repository, ke slot Tugas 6 di SCELE.

## Perintah commit dan push

Jalankan dari folder proyek. Kode DRF awal sudah ada pada riwayat Git sehingga tidak perlu dibuat ulang commit-nya. Perintah berikut khusus perubahan pelengkap pada pengerjaan ini. `.coverage` dan `test_e2e.py` yang sudah ada tidak ikut di-stage.

```powershell
git status --short
git add main/views.py templates/skill_form.html static/js/skill_edit.js
git commit -m "feat: melengkapi edit skill melalui API dan menyelaraskan hak akses"

git add main/tests_skill_api.py docs/tugas-6.md
git commit -m "feat: melengkapi pengujian akses dan checklist tugas enam"

git add README.md
git commit -m "feat: menambahkan jawaban reflektif tugas enam dan pengungkapan bantuan AI"

git push origin main
git log -1 --format="https://github.com/Albert-Timmothy/myportofolio/commit/%H"
```

Salin URL hasil perintah terakhir ke SCELE. Bila perlu memperbarui deployment PWS, jalankan `git push pws main` setelah push GitHub berhasil. Perintah tersebut tidak dijalankan oleh AI pada pengerjaan ini.
