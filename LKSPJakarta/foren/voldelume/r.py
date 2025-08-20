import pexpect
import sys

DEVICE = "lks.raw"
MAPPER_NAME = "lksvol"
WORDLIST = "/usr/share/wordlists/rockyou.txt"

with open(WORDLIST, "r", encoding="latin1") as f:
    for i, password in enumerate(f):
        password = password.strip()
        print(f"[{i}] Trying: {password}")

        child = pexpect.spawn(f"sudo cryptsetup luksOpen {DEVICE} {MAPPER_NAME}")
        try:
            child.expect("Enter passphrase for .*:", timeout=5)
            child.sendline(password)
            index = child.expect(["No key available with this passphrase", pexpect.EOF, pexpect.TIMEOUT], timeout=5)
            if index == 0:
                continue
            else:
                print(f"\n[+] SUCCESS! Password found: {password}")
                break
        except Exception as e:
            continue
