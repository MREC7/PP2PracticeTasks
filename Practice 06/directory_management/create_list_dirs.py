import os
os.mkdir("dir1")                           
os.makedirs("dir2/subdir", exist_ok=True)     
print(os.listdir("."))                       
os.chdir("dir1")                            
print(os.getcwd())                        
os.chdir("..")                            
os.rmdir("dir1")