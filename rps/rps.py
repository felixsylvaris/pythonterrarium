import random
# this is rock paper scissors game. Player can choose, pc is rolling. We have nice matrix of victory types. 

pclist=["rock","papper","scissors"]
transition={"rock":0,"papper":1,"scissors":2}
# vic matrix is player row, computer column , plnumber/pcnumber
vicmatrix=[[0,-1,1],
[1,0,-1],
[-1,1,0]]

def pcroll():
    pcchoice=random.choice(pclist)
    pcnumber=transition[pcchoice]
    return pcchoice,pcnumber

def plturn():
    print("""Pick your strategy.
    1) Rock 
    2) Papper 
    3) Scissors """)
    
    while True:
        plpick=input()
        
        if plpick in ("1","2","3"):
            break
        else:
            print("pick 1, 2 or 3")
    plnumber=int(plpick)-1
    plchoice= pclist[plnumber]
    print(f"You pcik {plchoice}")
    return plchoice,plnumber



def main():
    print("This is the game of rock, paper, scisor.")

    plchoice,plnumber=plturn()
    pcchoice,pcnumber=pcroll()
    
    resolution=vicmatrix[plnumber][pcnumber]
    print(f"You pick {plchoice}, computer choose {pcchoice}")
    print("The result is...")
    if resolution==1:
        print("You won!")
    elif resolution==-1:
        print("Computer Won!")
    else:
        print("It was a draw.")
    

while True:
    main()
    print("Do you want to play again? (y yes, n no")
    again=input()
    if again.lower()=="y":
        continue
    else:
        break
    
    
    
    
    
    
    
    
    
    
