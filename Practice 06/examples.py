import os
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
f = open("demofile.txt")
print(f.read())
with open("demofile.txt") as f:
  print(f.read()) 
f = open("demofile.txt")
print(f.readline())
f.close()
with open("demofile.txt") as f:
  print(f.read(5))
with open("demofile.txt") as f:
  print(f.readline())
with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())
with open("demofile.txt") as f:
  for x in f:
    print(x)
with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")
with open("demofile.txt") as f:
  print(f.read())
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
if os.path.exists("myfile.txt"):
  os.remove("myfile.txt")
else:
  print("The file does not exist")
with open("demofile.txt") as f:
  print(f.read())
  f = open("myfile.txt", "x")
os.remove("demofile.txt")
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist") 