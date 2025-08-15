from Registry import Registry

reg = Registry.Registry("chall.reg")
for key in reg.root().subkeys():
    print(key.path())
