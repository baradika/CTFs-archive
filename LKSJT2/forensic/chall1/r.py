import re

data = """
searchFor=L&goButton=go
searchFor=K&goButton=go
searchFor=S&goButton=go
searchFor=J&goButton=go
searchFor=T&goButton=go
searchFor=2&goButton=go
searchFor=%7B&goButton=go
searchFor=f&goButton=go
searchFor=0&goButton=go
searchFor=r&goButton=go
searchFor=3&goButton=go
searchFor=n&goButton=go
searchFor=-&goButton=go
searchFor=5&goButton=go
searchFor=1&goButton=go
searchFor=c&goButton=go
searchFor=_&goButton=go
searchFor=b&goButton=go
searchFor=4&goButton=go
searchFor=5&goButton=go
searchFor=1&goButton=go
searchFor=c&goButton=go
searchFor=_&goButton=go
searchFor=0&goButton=go
searchFor=n&goButton=go
searchFor=_&goButton=go
searchFor=n&goButton=go
searchFor=3&goButton=go
searchFor=t&goButton=go
searchFor=w&goButton=go
searchFor=o&goButton=go
searchFor=r&goButton=go
searchFor=k&goButton=go
searchFor=_&goButton=go
searchFor=p&goButton=go
searchFor=c&goButton=go
searchFor=4&goButton=go
searchFor=p&goButton=go
"""

chars = re.findall(r'searchFor=([^&]+)', data)
decoded = ''.join(chars)

from urllib.parse import unquote
decoded = unquote(decoded)

print(decoded)
