template = 'fn main(){let x="REPL";print!("{}{}{:?}{}",&x[..9],&x[9..17],x,&x[17..]);}'
for n in range(207, 0, -1):
    digits = "1" * n
    inner = f'fn main(){{let x=REPL;print!("{{}}{{}}{{:?}}{{}}",&x[..9],&x[9..17],x,&x[17..]);}}//CF=16{digits}'
    escaped = inner.replace("\\", "\\\\").replace('"', '\\"')
    code = template.replace("REPL", escaped)
    if 170 <= len(code) <= 181 and sum(int(c) for c in code if c.isdigit()) == 207:
        print(code)
        break
