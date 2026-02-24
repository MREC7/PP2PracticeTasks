n = 5
def square_generator(N):
    for i in range(N + 1):
        yield i * i
for value in square_generator(n):
    print(value)
def even_numbers(N):
    for i in range(N + 1):
        if i % 2 == 0:
            yield i
print(", ".join(str(num) for num in even_numbers(n)))
def divisible_by_3_and_4(N):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i
for num in divisible_by_3_and_4(n):
    print(num)
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
for value in squares(1, n):
    print(value)
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
for num in countdown(n):
    print(num)