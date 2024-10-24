import os
import glob
import shutil


# CREATE A BANNER FOR THE TOOL 
def ofid_banner():
    print(r"""

    ===============

    WELCOME TO OFID! Order Your Files Correctlly!

  ___  _____ ___ ____  
 / _ \|  ___|_ _|  _ \ 
| | | | |_   | || | | |
| |_| |  _|  | || |_| |
 \___/|_|   |___|____/ 
    

    Copyrights © 2024 All Rights Reserved by $SecDev_Zakaria

   =============== 
    """)
ofid_banner()

# LOOP UNTIL THE USER PROVIDES A VALID PATH
while True:
    pathA = input("Please enter the full path of the folder you want to organize: ")
    
    # CHECK IF THE PROVIDED PATH EXISTS
    if os.path.isdir(pathA):
        break  # If the path exists, exit the loop
    else:
        print(f"The path '{pathA}' does not exist. Please try again.\n")

# CONTINUE WITH THE REST OF THE SCRIPT ONCE A VALID PATH IS PROVIDED
# CREATE AN EMPTY SET AND LIST ALL FILES WITH THE 'GLOB' METHOD
mySet = set()
checkList = glob.glob1(pathA, '*.*')

# EXTRACT THE FILE EXTENSION USING 'SPLIT' METHOD AND ADD IT TO 'mySet'
for files in checkList:
    mySet.add(os.path.splitext(files)[1])

# CREATE A DIRECTORY WITH THE EXTENSION NAME (excluding the dot '.') INSIDE THE 'pathA' DIRECTORY
for exts in mySet:
    direcName = os.path.join(pathA, exts[1:])
    os.makedirs(direcName, exist_ok=True)  # exist_ok=True ensures that the directory is created if it doesn't already exist

    # MOVE FILES WITH THE CURRENT EXTENSION TO THE CORRECT DIRECTORY
    for dirpath, dirnames, filenames in os.walk(pathA):
        for exten in filenames:
            extension = os.path.splitext(exten)[1]
            if extension == exts:
                sourcePath = os.path.join(dirpath, exten)
                shutil.move(sourcePath, os.path.join(direcName, exten))

print("Files have been successfully organized by extension.")
