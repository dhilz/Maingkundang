# README - Auto Sign-Up Script

## Deskripsi
Script ini dibuat untuk melakukan proses otomatisasi pendaftaran akun Tesnet Suttt:
- Ekstraksi OTP dari email yang diterima.
- Penanganan pop-up secara otomatis.
- Penanganan error rate limit (HTTP 429).
- Rotasi User-Agent untuk menghindari deteksi aktivitas otomatis.
- Looping proses pendaftaran dengan jeda acak untuk menghindari deteksi.

---

## Persyaratan Sistem
1. Python 3.8 atau lebih baru.
2. Browser Google Chrome terinstal.
3. Koneksi internet aktif.
4. Pastikan Install chrome Webdriver Dulu Di Mari 
---
## Cara Install Chrome WebDriver
1. Pastikan Google Chrome Terinstal Unduh dan instal Google Chrome dari situs resmi: Google Chrome Download. Setelah instalasi, periksa versi Chrome Anda dengan membuka       Chrome dan mengetikkan chrome://settings/help di bilah alamat. Catat versi Chrome Anda.
2. Unduh Chrome WebDriver yang Sesuai Kunjungi situs resmi Chrome WebDriver: ChromeDriver Download. Unduh versi Chrome WebDriver yang sesuai dengan versi Chrome Anda.         Misalnya, jika versi Chrome Anda adalah 114.x, pilih ChromeDriver versi 114.x.
3. Ekstrak File Chrome WebDriver
    Ekstrak file yang diunduh (biasanya dalam format .zip) ke C:\chromedriver

## Instalasi
1. **Clone atau download repository ini.**
2. **Instal Python dan pip (jika belum ada).**
   - Pastikan Anda dapat menjalankan `python --version` dan `pip --version` di terminal/command prompt.

3. **Install dependencies.**
   Jalankan perintah berikut di terminal/command prompt:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment (opsional).**
   - Buat file `.env` di direktori yang sama dengan script ini.
   - Tambahkan variabel berikut (ganti dengan nilai Anda sendiri Terutama Di Bagian Refferall):
     ```env
     PASSWORD=Dilz@2408
     REFERRAL_CODE=678a148718fc9
     TIMEOUT=120
     ```

---

## Cara Menjalankan
1. Buka terminal/command prompt.
2. Jalankan script menggunakan perintah:
   ```bash
   python main.py
   ```

3. Proses akan berjalan secara otomatis, mencakup:
   - Membuat email sementara.
   - Mengisi formulir pendaftaran.
   - Mendapatkan dan memverifikasi OTP.
   - Menyelesaikan proses pendaftaran.
   - Mengulangi proses dengan jeda acak.

4. Untuk menghentikan script, tekan `Ctrl + C`.

---

## Fitur Utama
1. **Pembuatan Email Sementara**
   - Menggunakan library `temp-mails` untuk mendapatkan alamat email sementara.
   - Mendukung rotasi email jika dibatasi oleh layanan temp-mail.

2. **Penanganan OTP**
   - Ekstraksi OTP dari email HTML menggunakan `BeautifulSoup`.

3. **Rotasi User-Agent**
   - Menggunakan library `fake-useragent` untuk menghindari deteksi otomatisasi.

4. **Anti Rate-Limit**
   - Script secara otomatis menunggu dan mencoba kembali jika menerima error 429.

5. **Loop Pendaftaran**
   - Script berjalan dalam loop hingga dihentikan secara manual.

---

## Troubleshooting
1. **Error "Failed to create email, status 429"**
   - Layanan temp-mail sedang membatasi permintaan.
   - Solusi: Tunggu beberapa menit, script akan mencoba lagi secara otomatis.

2. **Error "WebDriver not found"**
   - Pastikan Google Chrome terinstal.
   - Pastikan Anda telah menginstal `webdriver-manager`.

3. **Tidak ada OTP di email**
   - Pastikan alamat email yang dibuat valid.
   - Layanan mungkin mengalami keterlambatan, script akan mencoba ulang secara otomatis.

4. **Proses lambat**
   - Script secara sengaja menambahkan jeda acak untuk menghindari deteksi.

---

## Lisensi
MIT LICENSE

---
## NOTE
**Jika Failed Get Email / Otp Nya Silahkan pakek Vpn Kemudian jalankan Lagi Di Karenakan Limit IP Oleh Penyedia Layanan Email Nya**
**Jika Ingin Menggunakan Secara Terus Menerus Tanpa Henti Sebaik Nya Menggunakan Ip Changer [https://github.com/seevik2580/tor-ip-changer](Github_Berikut)**
**Youtube Vidio Untuk Change Ip Otomatis Di Mari Btw Youtube Orang Wkk [https://youtu.be/qFRXqJZrsUM?si=k3S4Iv-n4JQpQ8pd](Youtube)**
**SECARA DEFAULT PROGRAM INI OPEN WEB JADI KALOK GAK MAU OPEN WEB ALIAS JALAN DI TERMINAL AJA HAPUS AJA AWALAN DI  #options.add_argument('--headless') DI MAIN.PY NYA**
