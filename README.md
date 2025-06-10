# ProjectAI_Orbi_AdminUserPage

Folder Structure Overview

AOL_ProjectAI_AdminUserPage/
├── app3.py                    # Main Flask web app (login, role-based access)
├── detectobject2.py          # Object detection process (YOLOv8)
├── readtext.py               # Text reading with OCR (EasyOCR)
├── requirement.txt           # List of dependencies
├── instance/
│   └── orbi.db               # SQLite database with user and activity_log tables
├── static/
│   └── orbi.png              # Logo for user and admin pages
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── user.html
│   └── admin.html

1. Installation Instructions
A. Python & Environment Setup
Install Python 3.8+:
Download from https://www.python.org/downloads/

Install dependencies from requirement.txt:

pip install -r requirement.txt

2. Running the Web Application
A. Start the Web Server
From the root folder AOL_ProjectAI_AdminUserPage, run:

python app3.py

A local server will run at:
http://127.0.0.1:5000 → buka di browser.

3. USER FLOW (Role: User)
A. Register & Login
Buka web: http://127.0.0.1:5000

Klik "Don't Have Account" -> Register

Isi: Username, Password, Role: user

Klik Register, lalu Login dengan akun tersebut.

Login

User dengan role user → diarahkan ke user.html.

User dengan role admin → diarahkan ke admin.html.



B. User Page (user.html)

Voice Command
Klik 🎤 Speak button, ucapkan:

"hello" → bot menyapa.

"detect object" → aktifkan deteksi objek.

"stop detecting object" → hentikan deteksi objek.

"read text" → mulai membaca teks dari gambar/kamera.
- Webcam terbuka
- klik 'C' untuk capture gambar
- sistem membacakan teks
- klik 'q' 2 kali di keyboard untuk keluar dari read text dan kembali ke Website

📍 Tampilkan Lokasi
Klik button 📍 Tampilkan Lokasi
→ akan menampilkan lokasi device secara detail dan mengucapkannya dengan TTS.
Lokasi disimpan ke activity_log.

📜 Activity Log
Ditampilkan di bawah tombol:

Jam (timestamp), Aksi terakhir, Lokasi

4. ADMIN FLOW (Role: Admin)
A. Register & Login sebagai Admin
Daftar akun dengan role admin

Login → dialihkan ke admin.html

B. Cari Username User yang ingin dilihat aktivitasnya
Langkah-langkah:
- Isi kolom pencarian dengan username yang ingin dicari.
- Klik tombol Cari

Scroll ke bawah:

Ditampilkan:

- Lokasi terakhir user di peta + teks lokasi

- Waktu terakhir user aktif

- Tabel aktivitas terakhir user (log dari orbi.db)

- Format tabel recent activities:
Time	Username	Action	Location

5. Deteksi Objek (YOLOv8) – detectobject2.py
Di-trigger oleh perintah suara "detect object"
Program akan:
- Capture gambar selama 10 detik sekali
- Deteksi objek secara real-time menggunakan YOLOv8
- Bot akan mengatakan "Detected: (objek yang terdeteksi)"

klik speak button lalu katakan “stop detecting object” → menghentikan proses

*Tes Manual:

python detectobject2.py

6. Pembaca Teks (OCR) – readtext.py
Di-trigger oleh perintah suara "read text"
Program akan:
- Ambil gambar dari webcam, user klik 'c' untuk capture gambar
- Baca teks di dalam gambar menggunakan EasyOCR
- Ucapkan teks hasil pembacaan (pyttsx3)
- klik 'q' untuk keluar dari program

* Tes Manual:

python readtext.py

7. Database Structure – orbi.db (SQLite)
Lokasi:
instance/orbi.db

Struktur Tabel:

CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(200) NOT NULL,
  role VARCHAR(20) NOT NULL
);

CREATE TABLE activity_log (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  action VARCHAR(255),
  location VARCHAR(100),
  timestamp DATETIME,
  FOREIGN KEY(user_id) REFERENCES user(id)
);

Notes
  Authentication
  Password dienkripsi dengan werkzeug.security.generate_password_hash

  Session-based login & role-checking

📍 Location Handling
Lokasi diambil dari browser (navigator.geolocation) → dikirim ke backend dan diubah jadi teks deskriptif via API Google Maps 

ogging
Semua aksi penting seperti:
- detect object
- read text
- get location

Dicatat ke tabel activity_log dengan user_id, timestamp, dan lokasi.

8. Logout & Ganti Akun
Klik tombol Logout.

Bisa register ulang atau login dengan akun berbeda.

