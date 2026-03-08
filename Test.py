import re

a = input()
esc = re.compile(r'\b\w+\b')
res = esc.findall(a)
print(len(res))