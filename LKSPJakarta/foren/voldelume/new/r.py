from pwn import remote, context
from Crypto.Util.number import bytes_to_long
import math
import sympy
import json

context.log_level = 'error'  # set ke 'debug' kalau mau lihat raw I/O

def solve():
    r = remote('13.212.62.29', 7716)

    # Terima initial hand dari server
    while True:
        data = r.recvline().decode().strip()
        try:
            hand = json.loads(data)['hand']
            break
        except:
            continue
    print("[+] Hand:", hand)

    # Cari 2 kartu selain FLAG of FLAG
    cards_clean = [card for card in hand if card != "FLAG of FLAG"]
    if len(cards_clean) < 2:
        print("Not enough clean cards!")
        return

    cards1 = [cards_clean[0]]
    cards2 = [cards_clean[1]]

    def get_token(cards):
        query = {
            "action": "get_token",
            "query": {
                "action": "play",
                "cards": cards
            }
        }
        r.sendline(json.dumps(query).encode())
        while True:
            resp = r.recvline().decode().strip()
            try:
                data = json.loads(resp)
                if 'token' in data:
                    return int(data['token'])
            except:
                continue

    s1 = get_token(cards1)
    s2 = get_token(cards2)
    print("[+] Sample cards:", cards1, cards2)

    m1 = bytes_to_long(f"play {json.dumps(cards1)}".encode())
    m2 = bytes_to_long(f"play {json.dumps(cards2)}".encode())

    # Recover e, n
    print("[*] Recovering e and n...")
    e = None
    n = None
    for e_candidate in sympy.primerange(3, 2**12):
        try:
            num = pow(m1, e_candidate) - s1
            den = pow(m2, e_candidate) - s2
            g = math.gcd(num, den)
            if g.bit_length() in (511, 512, 513):
                e = e_candidate
                n = g
                break
        except:
            continue

    if not e or not n:
        print("[-] Failed to recover RSA parameters")
        return
    print(f"[+] Found e = {e}")
    print(f"[+] Found n = {n}")

    # Buat forged token untuk FLAG
    target_cards = ["FLAG of FLAG"] * 5
    m_flag = bytes_to_long(f"play {json.dumps(target_cards)}".encode())
    token_flag = pow(m_flag, e, n)

    # Kirim play request untuk FLAG
    payload = {
        "action": "play",
        "token": str(token_flag),
        "cards": target_cards
    }
    r.sendline(json.dumps(payload).encode())

    while True:
        try:
            resp = r.recvline().decode().strip()
            if "flag" in resp.lower():
                print("[+] Got response:", resp)
                break
        except:
            continue

    r.close()

if __name__ == "__main__":
    solve()
