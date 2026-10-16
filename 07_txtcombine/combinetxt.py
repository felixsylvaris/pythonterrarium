"""
This program will read content of directory, ask politly to name two txt files. And combine them into new txt file. 
"""
import os

# Find the directory where this Python script is located
default_dir = os.path.dirname(os.path.abspath(__file__))

print("Working directory:", default_dir)
print("\nFiles available:")

# List files in our directory
files = os.listdir(default_dir)

for file in files:
    print(file)

# Ask the user to select two input files
print("This program will ask for names of two txt files. And combine them. Into new file.\n" ,
" Please make sure the files are in the same directory as this script.\n")
file1_name = input("\nEnter the name of file 1 (format: filename.txt): ")
file2_name = input("Enter the name of file 2 (format: filename.txt): ")

# Ask for the output filename
file3_name = input("Enter the name of the combined file (format: filename.txt): ")

# Build full paths
path1 = os.path.join(default_dir, file1_name)
path2 = os.path.join(default_dir, file2_name)
path3 = os.path.join(default_dir, file3_name)

# Check whether input files exist
if not os.path.isfile(path1) or not os.path.isfile(path2):
    print("Error: One or both input files do not exist.")

elif os.path.abspath(path3) in (
    os.path.abspath(path1),
    os.path.abspath(path2)
):
    print("Error: Output file cannot overwrite an input file.")

else:
    # Read both input files
    with open(path1, "r", encoding="utf-8") as file1:
        content1 = file1.read()

    with open(path2, "r", encoding="utf-8") as file2:
        content2 = file2.read()

    # Combine contents
    content3 = content1 + "\n" + content2

    # Write the combined content
    with open(path3, "w", encoding="utf-8") as file3:
        file3.write(content3)

    print("\nCombined file created:", path3)

    # Verify the result
    with open(path3, "r", encoding="utf-8") as check_file:
        print("\nCombined content:")
        print(check_file.read())
