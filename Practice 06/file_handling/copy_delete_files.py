import os, shutil
shutil.copy("demofile.txt", "example.txt")
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")
shutil.copy("example.txt", "demofile.txt")