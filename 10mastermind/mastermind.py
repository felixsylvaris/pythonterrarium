"""
This is the game about guessing password. Mastermind game
We write our suggestion, and it is judged, and scored. 
1 - this word success, 
+0.05 good place
+0.04 good letter wrong place
-0,039 each letter off lenght
Note good letter good place sums to 0.09 
We can have only as good good letters as either in target or attempt. 
We can see last 10 attempts adn scores. And even all of them. 
"""

from random import choice

words_pile=["hello world","goodbye world"]
ALLOWED = set("abcdefghijklmnopqrstuvwxyz ")
secretword=choice(words_pile)
tried = []
ntries=0 


print("""This is the game.
You need to guess secret password.
Tips: It contains only a-z letters and maybe space, and is less <30 letters.
Special keys: 1 - see all tried attempts, 0 - exit 
Score: 1 is perfect and win. """)



def quick_show():
    for piece in tried[-10:]:
        print(piece)
        
        
def long_show():
    print(tried)

def freq_dict_maker(victim):
    # this is func helper to deconstruct string into freq dict
    #  there is c = Counter(victim) but our scientist havent unlocked it yet  
    
    work={}
    
    for i in victim:
        if i in work:
            work[i] += 1 
        else:
            work[i] = 1
    return work
        

def judge(attempt):
    # this func counts score how close we are to target word
    # 0.09 good letter good position 0.04 good letter wrong position -0.039 len off each
    # cap on how many good letters we can have, no more than exist in target 
    if attempt==secretword:
        return 1
    if len(attempt)==0:
        return len(secretword)*(-0.039)
    score=0 
    # first check lenght
    score += abs(len(secretword)-len(attempt))*(-0.039)
    
    for i in range(min(len(secretword),len(attempt))):
        if attempt[i]==secretword[i]:
            score += 0.05
    
    att_dict=freq_dict_maker(attempt)
    
    for j in att_dict:
        if j in target_dict:
            score += min(target_dict[j],att_dict[j]) * 0.04
    # this is intended we get 0.05 for correct position, and 0.04 for letter number
    return score
    
def victory():
    # this triggers when we won 
    print("You guessed secret word! ")
    print(f" It was {secretword} all along.")
    print(f"It took only {ntries} attempts ")
    quit()

def quickexit():
    print("Not every day is full of victories.")
    print(f" The word was {secretword}. You ware so close.")
    quit()

def main():
    #Main gaming loop. ask for words.
    global ntries
    
    while True:
        print("This is the game where you have to guess secret word.")
        print("Tips: word contains only a-z and space, and is less than 30 chars.")
        print("Last 10 words:")
        quick_show()
        print("Try next, type 1 for all attempts, 0 to exit")
        while True:
            ans=input("next attempt:")
            if len(ans)>30:
                print("30 character or less")
            elif not ans.strip():
                print("You need try something")
            elif ans=="1":
                long_show()
            elif ans=="0":
                quickexit()
            elif set(ans) <= ALLOWED:
                temp=round(judge(ans),3)
                pack=(ans, temp )
                ntries += 1
                tried.append(pack)
                print(f"You tried '{ans}' and got {temp} score. ")
                if ans==secretword:
                    victory()
                    break
                if ans!=secretword and temp==1:
                    print("Your score is 1 but word is different. ")
                break 
            else:
                print("Something went wrong, type again. ")
                    
                
                
        
        
    
# ACTIONS HERE
target_dict=freq_dict_maker(secretword)


if __name__ == "__main__":
    main()


    
    



    
