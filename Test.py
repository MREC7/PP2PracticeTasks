names = ["Ivan","Anna","Oleg"]
scores = [80,95,70]
a = zip(names, scores)
print("{")
for i, k in a:
    print(f"\"{i}\":{k}")
print("}")