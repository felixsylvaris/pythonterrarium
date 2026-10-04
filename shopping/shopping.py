"""
Hello world
This is shoping grocery simulator.
edupoint: function jumping, and fancy dict. 
To Do:
1. Shop1 dictionary with items, and shop2. Inventory empty, cash var. Menu. 
2. Shop in the shop buy
3. Menu navigation
4. Sell in shop
5. Go home and resolution
"""

from sys import exit

goods=("apples","bread","butter",
"cheese","eggs","flour",
"milk","pasta","sausage")

menu_list=("1","2","3","4")

lookup = {
    "1": "apples",
    "apples": "apples",
    "2": "bread",
    "bread": "bread",
    "3": "butter",
    "butter": "butter",
    "4": "cheese",
    "cheese": "cheese",
    "5": "eggs",
    "eggs": "eggs",
    "6": "flour",
    "flour": "flour",
    "7": "milk",
    "milk": "milk",
    "8": "pasta",
    "pasta": "pasta",
    "9": "sausage",
    "sausage": "sausage"
}

shop1 = {
    "apples":  {"price": 2.46, "stock": 200},
    "bread":   {"price": 1.89, "stock": 100},
    "butter":  {"price": 3.29, "stock": 80},
    "cheese":  {"price": 4.75, "stock": 60},
    "eggs":    {"price": 2.99, "stock": 120},
    "flour":   {"price": 1.49, "stock": 150},
    "milk":    {"price": 1.79, "stock": 100},
    "pasta":   {"price": 2.19, "stock": 130},
    "sausage": {"price": 5.49, "stock": 70}
}

shop2 = {
    "apples":  {"price": 2.89, "stock": 140},
    "bread":   {"price": 1.59, "stock": 180},
    "butter":  {"price": 3.75, "stock": 55},
    "cheese":  {"price": 4.29, "stock": 90},
    "eggs":    {"price": 3.49, "stock": 75},
    "flour":   {"price": 1.29, "stock": 200},
    "milk":    {"price": 2.09, "stock": 65},
    "pasta":   {"price": 1.79, "stock": 160},
    "sausage": {"price": 4.99, "stock": 45}
}

cash=100
bag={}

def menu():
    print(f"""You have {cash}$, where do you go?

1) Shop 1
2) Shop 2
3) Inventory
4) Home
""")
# force correct input
    while True:
        ans1=input("Pick number 1-4 ")
        if ans1 in menu_list:
            break
        else:
            print("Need to pick number 1-4 ")
    
    # use ans1 now
    if ans1=="1":
        shopping(shop1)
    elif ans1=="2":
        shopping(shop2)
    elif ans1=="3":
        inventory()
        
    elif ans1=="4":
        home()

def inventory():
    print(f"You have {cash} $ in your pockets. Your shopping bag contains:")
    cnt=1
    for key,value  in bag.items():
        print(f"{cnt}. {key}: {value} \n")
        cnt+=1
    if not bag or sum(bag.values())==0 :
        print("Your bag is empty. Buy something NOW!")
    return
        
 

def home():
    print(f"You came home. You still have {cash} $ in the wallet.")

    if not bag or sum(bag.values()) == 0:
        print("You haven't bought anything in the end. "
              "But tomorrow is another day.")
    else:
        print("You managed to buy:")
        for key, value in bag.items():
            print(f" {key}: {value}")

        print("This will keep you alive for some time.")

    exit()
    
def shopping(place):
    global cash
    while True:
        
        print("You came to the shop. You can buy here:")
        cnt=1
        for key,value  in place.items():
            print(f"{cnt}. {key}: {value} \n")
            cnt+=1
        print("0. Exit shop \n")
        
   
        
        while True:
            ans2=input("What you want to buy?")
            if ans2.lower() in lookup:
                ans2=ans2.lower()
                ans2 = lookup[ans2]
   
                break
            elif ans2=="0":
                break
            else:
                print("Pick valid item from list")
        if ans2=="0":
            break
        
        while True:
            ans3 = input("How many " + ans2 + " do you want to buy? ")
        
            try:
                ans3 = int(ans3)
                if ans3 > 0 and ans3<=place[ans2]["stock"] :
                    
                    break
                elif ans3>place[ans2]["stock"]:
                    print("The shop has not that many. Pick less. ")
                    continue
            except ValueError:
                pass

            print("Enter a positive whole number.")
        
        if ans2 not in bag:
            bag[ans2] = 0
        
        
        cost=place[ans2]["price"]*ans3
        if cost>cash:
            print("That is too much! Pick less or cheaper product.")
        else:
            cash-=cost
            place[ans2]["stock"]-=ans3
            bag[ans2]+=ans3
            print(f"You bought {ans3} {ans2} for {cost} $. You have {cash} $ left")
        
            
        
# ACTUAL PROGRAM LOOP HERE

while True:
    menu()
            
    
        
    
    
    
    

        
    
    
  
    


