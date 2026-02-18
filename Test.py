def squares(a, n):
    for i in range(0, n):
        yield a
a = input()
n = int(input())
print(*(list(squares(a, n))))