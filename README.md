![gambar](https://github.com/user-attachments/assets/24eee300-ac63-4a8c-b778-688da461a6ec)

# Brute Force VPN - PPTP
Tools Bruteforce VPN Method PPTP
# VPN Testing Tools

VPN Testing Tools adalah sebuah script Python yang digunakan untuk melakukan pengujian konektivitas VPN, menguji kebocoran DNS, mengukur kecepatan internet, serta melakukan brute-force login pada VPN PPTP di Linux.

## Fitur
- **Auto-install Dependencies:** Secara otomatis menginstal paket-paket Python yang diperlukan (seperti `colorama`, `requests`, `speedtest-cli`, dan `tqdm`).
- **Validasi Sistem:** Memeriksa sistem operasi (hanya mendukung Linux) dan mengecek ketersediaan dependensi sistem seperti `pptpsetup` dan `nmap`.
- **Connectivity Test:** Menguji konektivitas dengan melakukan ping ke host (default: 8.8.8.8).
- **DNS Leak Test:** Mengambil IP publik dan informasi lokasi menggunakan API online.
- **Speed Test:** Mengukur kecepatan unduh dan unggah internet menggunakan modul `speedtest-cli`.
- **Brute-force VPN PPTP:** Mencoba kombinasi username dan password dari wordlist untuk brute-force login ke VPN PPTP.

## Prasyarat
- **Sistem Operasi:** Linux
- **Python:** Python 3.x
- **Hak Akses:** Akses sudo mungkin diperlukan untuk menginstal paket sistem (misalnya, `pptp-linux` dan `nmap`).

## Instalasi & Penggunaan

1. **Clone Repository**

   Clone repository ini ke komputer kamu:
   ```bash
   git clone https://github.com/YourUsername/VPNTestingTools.git
2. **Masuk ke Direktori**
   ```bash
   cd VPNTestingTools
3. **Beri Hak Eksekusi (Opsional)**
   ```bash
   chmod +x vpn_testing_tools.py
4. **Jalankan Script**
   ```bash
   ./vpn_testing_tools.py

   atau
  
   python3 vpn_testing_tools.py


## Menu Opsi

Setelah menjalankan script, kamu akan diberikan opsi menu seperti:

    1. Connectivity Test: Melakukan ping ke host yang ditentukan (default: 8.8.8.8).
    2. DNS Leak Test: Mengambil dan menampilkan IP publik beserta informasi lokasi.
    3. Speed Test: Mengukur kecepatan unduh dan unggah internet.
    4. Brute-force VPN (PPTP): Mencoba login ke VPN PPTP dengan kombinasi username dan password dari wordlist.

## Lisensi

Script ini dibuat oleh Majalengka Cyber Tester dan didistribusikan secara bebas untuk keperluan pengujian keamanan.
