from Crypto.Cipher import AES
from Crypto.Util.number import *
import os

key = os.urandom(16)
iv = 'heheAEStheticheh'
flag = "COMPFEST17{this_is_fake_flag}"

assert len(flag) % 16 == 0
assert len(iv) == 16

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv.encode())
    return cipher.encrypt(data)

def decrypt(data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data).hex()

def show_banner():
    print("=" * 21 + "°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･" + "=" * 21)
    print(" " * 12 + "🌸 Welcome to AESthetic Decryptor 🌸")
    print(" " * 16 + "Everything is aesthetic here!")
    print("=" * 21 + "°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･" + "=" * 21)

def print_menu():
    print("""❋ Menu ❋
1. Decrypt
2. Encrypt Flag
3. Decrypt Flag
4. Leave""")

def main():
    show_banner()

    while True:
        try:
            print_menu()
            choice = input("> ")
            if(choice == '1'):
                print("⚘ Hex only yaw ⚘")
                inp = input("> ")
                print("Here is the result: " + decrypt(bytes.fromhex(inp)) + "\n")
            elif(choice == '2'):
                enc_flag = encrypt(flag.encode())
                print(f"Here is the flag: {[enc_flag[i:i+16] for i in range(0, len(enc_flag), 16)]}\n")
            elif(choice == '3'):
                print("Ooops no no ya! Do it by yourself ok? ☘︎\n")
            elif(choice == '4'):
                print("❀ See youu ❀\n")
                break
            else:
                print("Invalid input :(\n")
        except:
            print("Oh noo, bye ִֶָ𓂃 ࣪˖ ִִֶֶָ🥀་༘࿐\n")
            break

if __name__ == "__main__":
    main()