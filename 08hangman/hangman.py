

import random
source_list=["january"]
work_list=source_list.copy()

MAX_LIVES=7
lives=MAX_LIVES

#init
word=random.choice(work_list)
print(word)

list_word=list(word)
mask=["_"]*len(word)


tofind=len(list_word)
seen=[]

print("Lets play the game.")

while lives>0 and tofind>0:
    print("Word to find \n" + str(mask))
    print("We tried: "+ str(seen))
    print("We have "+ str(lives) +" lives left.")
    print("pick your letter")
    print("We have to find: "+ str(tofind) )
    while True:
        ans=input().lower()
        if len(ans)!=1:
            print("ONE letter")
        elif ans in seen:
            print("New letter maybe?")
        else:
            break
    
    
    seen.append(ans)
    
    if ans not in list_word:
        lives-=1
    
    for i in range(len(list_word)):
        if ans==list_word[i]:
            tofind-=1
            mask[i]=ans
            
    if lives==0:
        print("You lost, better luck next time")
    
    if tofind==0:
        print("You absolutly won everything!")
        break
    
    
    
    
    






