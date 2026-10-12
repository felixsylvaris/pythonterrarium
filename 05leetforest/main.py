"""
ABOUT
Plot: A little Necromancer Witch travels through the Leet Forest.
She wants to reach her grandmother to deliver a food basket.

Code:
- Binary-tree-style navigation using Node objects. (it is more like graph, but shhh)
- A dictionary to load scene functions.
- OOP for witch and monster handling.
"""


# CREATURE CLASSES

class Creature:
    def __init__(self, name, power, maxhp, **kwargs):
        self.name = name
        self.power = power
        self.max_hp = maxhp
        self.temp_hp = self.max_hp
        self.idle_call = kwargs.get("idle_call", "roars and looks at the enemy with hostile intent.")
        self.attack_call = kwargs.get("attack_call", "attacks with all its strength.")

    def attack(self, target):
        print(f"{self.name} {self.attack_call}")
        target.temp_hp = max(0, target.temp_hp - self.power)

    def idle(self):
        print(f"{self.name} {self.idle_call}")


class Witch(Creature):
    def __init__(self, name, power, maxhp, **kwargs):
        # Witch-specific default dialogue
        kwargs.setdefault("idle_call", "leans on her staff, gathering power for the next spell.")
        kwargs.setdefault("attack_call", "swings the staff and blasts a magic ray.")
        super().__init__(name, power, maxhp, **kwargs)

        self.gold = kwargs.get("gold", 0)
        self.inventory = {}

    def drain_life(self, target):
        print(f"{self.name} uses her magic to drain life from {target.name}.")
        damage = max(0, self.power - 2)
        self.temp_hp = min(self.max_hp, self.temp_hp + 2)
        target.temp_hp = max(0, target.temp_hp - damage)


# COMBAT

def show_hp(player, enemy):
    print(f"\n{player.name}: {player.temp_hp}/{player.max_hp} HP | "
          f"{enemy.name}: {enemy.temp_hp}/{enemy.max_hp} HP")


def mortal_kombat(player, enemy):
    print(f"{player.name} stands against {enemy.name}. The fight can't be avoided.")

    while player.temp_hp > 0 and enemy.temp_hp > 0:
        show_hp(player, enemy)

        # Player turn
        player.idle()

        while True:
            ans = input("Choose attack \n 1) magic blast \n 2) life drain \n")
            if ans in ("1", "2"):
                break
            print("Pick a valid answer.")

        if ans == "1":
            player.attack(enemy)
        else:
            player.drain_life(enemy)

        # Monster turn
        if enemy.temp_hp > 0:
            enemy.idle()
            enemy.attack(player)

    if player.temp_hp <= 0:
        print(f"{player.name} is dead. What a sad end.")
    else:
        print(f"{enemy.name} is dead. You can move forward.")


# SCENE FUNCTIONS

def glade01(player):
    print("This is definitely a nice-looking glade.")


def dark_path(player):
    print("A wild goblin appears, but is too confused to attack.")
    goblin1 = Creature("Goblin", 3, 8,
                       idle_call="stares at you, clearly lost.",
                       attack_call="flails its club half-heartedly.")
    mortal_kombat(player, goblin1)


def stream(player):
    print("Walking along the stream is peaceful.")
    print("Oh look, there is a gold nugget among the stones.")
    player.gold += 5


def grama_grave(player):
    print("You reach your grandmother's grave.")
    print("You place the food on the tombstone.")
    print("Even wicked dead deserve rest.")


# SCENE LOOKUP

scenes = {
    "glade1": glade01,
    "dark_path": dark_path,
    "stream": stream,
    "gramma": grama_grave,
}


# NAVIGATION

class Node:
    def __init__(self, nodename, left=None, right=None, textto=""):
        self.nodename = nodename
        self.left = left
        self.right = right
        self.textto = textto


# BUILD THE FOREST

start_node = Node("glade1", textto="The glade among Leet Forest.")
dark = Node("dark_path", textto="Go down the dark path.")
stream_node = Node("stream", textto="Follow the stream.")
end_node = Node("gramma", textto="You see a familiar graveyard.")

start_node.left = dark
start_node.right = stream_node

dark.left = end_node
stream_node.left = end_node


def path_choice(now_node):
    choices = {}

    if now_node.left is not None:
        choices["1"] = now_node.left

    if now_node.right is not None:
        choices["2"] = now_node.right

    print("\nWhere do you go next?")

    for key, destination in choices.items():
        print(f"{key}) {destination.textto}")

    while True:
        ans = input("> ")

        if ans in choices:
            return choices[ans]

        print("Pick from: " + ", ".join(choices.keys()))


# MAIN LOOP

def main():
    now_node = start_node
    witch = Witch("Morgana", 4, 10)

    print("Little witch enters dark Leet Forest. \nTo deliver food basket for her grandma.")
    print("She sees a spot of light between dark trunks.")

    while True:
        # Load and execute the current scene
        scenes[now_node.nodename](witch)

        if witch.temp_hp <= 0:
            print("GAME OVER")
            break

        # Stop when we reach the grandmother's grave
        if now_node is end_node:
            print("\nYou completed the game!")
            break

        # Choose the next node
        now_node = path_choice(now_node)


if __name__ == "__main__":
    main()
