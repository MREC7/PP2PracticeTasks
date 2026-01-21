a = input()
b = input()
c = a.split(" ")
def check(c, b):
    if c == b:
        return True
    return False
print(check(c[1], b))
