
import random
import sys


def roll():
    result=random.randint(1,6)
    return result
    


while True:
    print("Do you want to play the game? Y/N")
    ans=input()
    
    if ans in ('y','Y'):
        break
    elif ans in ('n','N'):
        sys.exit()
    else:
        print("Write Y/N. ")
        
game=True


while game:
    plsum=0
    pctarget=random.randint(9,18)
    print("The game is to get as close to 21 as possible, but not above.")
    
    while True:
        print(f"Your value now is... {plsum}" )
        print("Do you want to roll? Y/N")
        ans2=input()
        
        if ans2 in ('Y','y'):
            roll2=roll()
            plsum+=roll2
            print(f"You roll {roll2} and your sum is {plsum} .")
            if plsum>21:
                print("You roll too much. You lose.")
                break
        else:
            
            print(f"Your value is {plsum}. Computer value is {pctarget}")
            if plsum>21 or plsum<pctarget:
                print("You lose!")
            elif plsum==pctarget:
                print(f"You and opponent both got {plsum}. That is draw.")
            else:
                print("You won.")
            break
        
    
    print("Do you want to play again? Y/N")
    ans3=input()
    if ans3 in ('y','Y'):
        continue
    else:
        game=False
        break
  
    


