import math
a = int(input("Input degree: "))
print(f"Output radian: {round(math.radians(a), 6)}")
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area = ((base1 + base2) / 2) * height
print("Expected Output:", area)
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area = (n * s ** 2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area))
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = base * height
print("Expected Output:", float(area))