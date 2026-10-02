
# Online Python - IDE, Editor, Compiler, Interpreter

import data as d



name = input("Enter your name:")
print(f"Hello {name}")

while True:
    print(f"What is your faction?")
    faction=input()
    
    if faction in d.credential.keys():
        print(f"You have the touch {name}. \n ")
        break
    else:
        print(f"The point is you are the fool. Again! \n")
        
while True:
    print("Write the password")
    password=input()
    
    if password==d.credential[faction]:
        print(f"You have the power! \n" 
        f"Secret messege incoming...\n \n"
        f"{d.message[faction]}")
        break
    else:
        print("Computer says... noooo. Again. ")
        
print("End of mission. Press anything.")
anything=input()
        
        
    