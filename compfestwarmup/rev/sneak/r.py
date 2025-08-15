import marshal
import types
import dis

with open("out.pyc", "rb") as f:
    f.read(16)  # skip header (magic + timestamp + size)
    code = marshal.load(f)

def recursive_disassemble(co, indent=0):
    pad = " " * indent
    print(f"{pad}Code object: {co.co_name}")
    print(f"{pad}Filename: {co.co_filename}")
    print(f"{pad}First line: {co.co_firstlineno}")
    print(f"{pad}Constants:")
    for const in co.co_consts:
        if isinstance(const, types.CodeType):
            recursive_disassemble(const, indent + 4)
        else:
            print(f"{pad}  {const!r}")
    print(f"{pad}Disassembly:")
    dis.dis(co)
    print()

recursive_disassemble(code)
