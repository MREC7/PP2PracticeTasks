import shutil
import os
os.mkdir("folder")
with open("test.txt", "w") as f:
    f.write("data")
shutil.move("test.txt", "folder/test.txt")