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

def order_by_extension():

    # LOOP UNTIL THE USER PROVIDES A VALID PATH
    while True:
        pathA = input("Please enter the full path of the folder you want to organize: ")
        
        # CHECK IF THE PROVIDED PATH EXISTS
        if os.path.isdir(pathA):
            break  # If the path exists, exit the loop
        else:
            print(f"The path '{pathA}' does not exist. Please try again.\n")
    
    # CREATE AN EMPTY SET AND LIST ALL FILES WITH THE 'GLOB' METHOD
    mySet = set()
    checkList = glob.glob1(pathA, '*.*')  # Gets a list of all files with extensions

    # EXTRACT THE FILE EXTENSION USING 'SPLIT' METHOD AND ADD IT TO 'mySet'
    for files in checkList:
        mySet.add(os.path.splitext(files)[1])  # Add the file extension to the set

    # CREATE A DIRECTORY WITH THE EXTENSION NAME (excluding the dot '.') INSIDE THE 'pathA' DIRECTORY
    for exts in mySet:
        direcName = os.path.join(pathA, exts[1:])  # Directory name based on the extension
        os.makedirs(direcName, exist_ok=True)  # Create the directory if it doesn't already exist

        # MOVE FILES WITH THE CURRENT EXTENSION TO THE CORRECT DIRECTORY
        for dirpath, dirnames, filenames in os.walk(pathA):
            for exten in filenames:
                extension = os.path.splitext(exten)[1]
                if extension == exts:
                    sourcePath = os.path.join(dirpath, exten)  # Get the source file path
                    shutil.move(sourcePath, os.path.join(direcName, exten))  # Move the file to the new directory

    print("Files have been successfully organized by extension.")

order_by_extension()