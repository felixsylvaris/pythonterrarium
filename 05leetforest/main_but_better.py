"""
THE LITTLE NECROMANCER WITCH AND THE LEET FOREST  (main_but_better.py)

Plot: Morgana, a tiny (chibi) Necromancer Witch, travels through the Leet Forest
to deliver a food basket to her grandmother... who is very, very dead.
Nobody told the forest that dead grandmas still like snacks.

What's new compared to the first version:
- Many more places (the forest is now a proper little graph, shhh).
- Four combat skills: magic blast, life drain, raise skeleton, flee (+ items).
- Mana, XP and level-ups.
- An inventory with potions, cookies and a very important jar of jam.
- A shop run by a very opinionated cat.
- Monsters with their own special behaviour (OOP: subclasses override methods).
- A boss and two different endings.

Code overview:
- Creature / Witch / Monster classes (OOP for witch and monster handling).
- Node objects form the map. Each node has a scene name and a list of exits.
- A dictionary maps scene names to scene functions ("scene lookup").
- A small input helper so the game never crashes on a bad keypress.
"""

import random
import sys


# =============================================================================
# INPUT HELPER
# =============================================================================

def ask(prompt, valid):
    """
    Keep asking until the player types one of the `valid` answers.
    Also handles Ctrl+D / closed input gracefully instead of crashing.
    """
    while True:
        try:
            ans = input(prompt).strip().lower()
        except EOFError:
            print("\n(The forest fades away... goodbye, little witch!)")
            sys.exit(0)
        if ans in valid:
            return ans
        print("Pick from: " + ", ".join(valid))


# =============================================================================
# CREATURE CLASSES
# =============================================================================

class Creature:
    """Anything that can fight: the witch, goblins, trolls, ghosts of dogs..."""

    def __init__(self, name, power, maxhp, **kwargs):
        self.name = name
        self.power = power
        self.max_hp = maxhp
        self.temp_hp = self.max_hp
        self.idle_call = kwargs.get("idle_call", "roars and looks at the enemy with hostile intent.")
        self.attack_call = kwargs.get("attack_call", "attacks with all its strength.")

    def is_alive(self):
        return self.temp_hp > 0

    def roll_damage(self, base):
        """Add a little randomness: base damage -1, +0 or +1 (never below 1)."""
        return max(1, base + random.randint(-1, 1))

    def take_damage(self, amount):
        """Lower HP, but never below zero."""
        self.temp_hp = max(0, self.temp_hp - amount)

    def heal(self, amount):
        """Raise HP, but never above the maximum."""
        self.temp_hp = min(self.max_hp, self.temp_hp + amount)

    def attack(self, target):
        print(f"{self.name} {self.attack_call}")
        target.take_damage(self.roll_damage(self.power))

    def idle(self):
        print(f"{self.name} {self.idle_call}")

    def take_turn(self, target):
        """
        What a creature does on its turn. Default: idle flavour text + attack.
        Monsters with special behaviour override this method.
        """
        self.idle()
        self.attack(target)


class Witch(Creature):
    """Morgana, our heroine. Has mana, gold, an inventory, XP and a skeleton buddy."""

    def __init__(self, name, power, maxhp, **kwargs):
        # Witch-specific default dialogue
        kwargs.setdefault("idle_call", "leans on her staff, gathering power for the next spell.")
        kwargs.setdefault("attack_call", "swings the staff and blasts a magic ray.")
        super().__init__(name, power, maxhp, **kwargs)

        self.gold = kwargs.get("gold", 0)
        self.inventory = {}            # item name -> how many we carry
        self.max_mana = 6
        self.mana = self.max_mana
        self.level = 1
        self.xp = 0
        self.minion_turns = 0          # how many more turns the skeleton fights for us
        self.skills = {"blast", "drain"}   # more skills can be learned in the forest
        self.flags = set()             # remembers one-time events ("already took the nugget")

    # ---- skills --------------------------------------------------------------

    def drain_life(self, target):
        print(f"{self.name} uses her magic to drain life from {target.name}.")
        damage = max(1, self.power - 2)
        self.heal(2)
        target.take_damage(damage)

    def raise_skeleton(self):
        """Necromancy! A tiny skeleton fights alongside her for a few turns."""
        print(f"{self.name} whispers a spell. A tiny skeleton claws out of the dirt and salutes!")
        self.minion_turns = 3

    def skeleton_attack(self, target):
        """Called once per round while the skeleton is still standing."""
        if self.minion_turns > 0:
            print("Bonehead the skeleton whacks the enemy with a femur. Clack!")
            target.take_damage(self.roll_damage(2))
            self.minion_turns -= 1
            if self.minion_turns == 0:
                print("Bonehead waves goodbye and crumbles back into a neat pile of bones.")

    # ---- inventory -----------------------------------------------------------

    def add_item(self, item, count=1):
        self.inventory[item] = self.inventory.get(item, 0) + count

    def has_item(self, item):
        return self.inventory.get(item, 0) > 0

    def use_item(self, item):
        """Remove one of an item. Returns True if we actually had it."""
        if not self.has_item(item):
            return False
        self.inventory[item] -= 1
        return True

    # ---- progression ---------------------------------------------------------

    def gain_xp(self, amount):
        self.xp += amount
        print(f"(+{amount} XP)")
        # Need level*10 XP to level up. A loop, in case one fight gives a lot.
        while self.xp >= self.level * 10:
            self.xp -= self.level * 10
            self.level += 1
            self.max_hp += 3
            self.power += 1
            self.max_mana += 1
            self.temp_hp = self.max_hp
            self.mana = self.max_mana
            print(f"*** LEVEL UP! {self.name} is now level {self.level}! "
                  f"Her hat grows a tiny bit pointier. ***")


# ---- special monsters --------------------------------------------------------

class Monster(Creature):
    """Base class for enemies. Adds XP/gold rewards and whether you may run away."""

    def __init__(self, name, power, maxhp, xp=5, gold=0, can_flee=True, **kwargs):
        super().__init__(name, power, maxhp, **kwargs)
        self.xp_reward = xp
        self.gold_reward = gold
        self.can_flee = can_flee


class Slime(Monster):
    """A blobby slime that heals a little every turn. Hit it hard!"""

    def take_turn(self, target):
        self.idle()
        self.heal(1)
        print(f"{self.name} jiggles and soaks up some swamp goo (+1 HP).")
        self.attack(target)


class Gloomhound(Monster):
    """
    The graveyard guard dog. Every third turn it howls and hits twice as hard,
    so the player gets a little warning before the big attack.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_counter = 0

    def take_turn(self, target):
        self.turn_counter += 1
        if self.turn_counter % 3 == 2:
            print(f"{self.name} inhales deeply... something BIG is coming!")
        if self.turn_counter % 3 == 0:
            print(f"{self.name} HOWLS and lunges with spectral jaws!")
            target.take_damage(self.roll_damage(self.power * 2))
        else:
            self.idle()
            self.attack(target)


# =============================================================================
# COMBAT
# =============================================================================

def show_hp(player, enemy):
    print(f"\n{player.name}: {player.temp_hp}/{player.max_hp} HP, "
          f"{player.mana}/{player.max_mana} MP | "
          f"{enemy.name}: {enemy.temp_hp}/{enemy.max_hp} HP")


def use_item_menu(player):
    """
    Let the player drink tea or eat a cookie. Returns True if a turn was used,
    False if they backed out (so backing out doesn't waste the turn).
    """
    usable = {"soul tea": "heals 8 HP", "moon cookie": "restores 4 MP"}
    options = {}
    for i, (item, effect) in enumerate(usable.items(), start=1):
        if player.has_item(item):
            options[str(i)] = item
            print(f"  {i}) {item} x{player.inventory[item]} ({effect})")
    if not options:
        print("Your pockets hold nothing useful. Only lint.")
        return False
    print("  0) never mind")
    ans = ask("> ", list(options.keys()) + ["0"])
    if ans == "0":
        return False

    item = options[ans]
    player.use_item(item)
    if item == "soul tea":
        player.heal(8)
        print("Slurp! The tea tastes like lavender and a faint whiff of regret. +8 HP.")
    else:
        player.mana = min(player.max_mana, player.mana + 4)
        print("Nom! The cookie sparkles on the way down. +4 MP.")
    return True


def choose_action(player, enemy):
    """
    Show the attack menu and run the chosen action.
    Returns "done" (turn used), or "fled" if the witch ran away successfully.
    """
    while True:
        print("Choose your move:")
        print(" 1) magic blast (free)")
        print(" 2) life drain (2 MP)")
        valid = ["1", "2", "4", "5"]
        if "skeleton" in player.skills:
            print(" 3) raise skeleton (3 MP)")
            valid.append("3")
        print(" 4) use item")
        print(" 5) run away!")
        ans = ask("> ", valid)

        if ans == "1":
            player.attack(enemy)
            return "done"

        if ans == "2":
            if player.mana < 2:
                print("Not enough mana! Your staff just fizzles sadly.")
                continue
            player.mana -= 2
            player.drain_life(enemy)
            return "done"

        if ans == "3":
            if player.mana < 3:
                print("Not enough mana for necromancy today.")
                continue
            if player.minion_turns > 0:
                print("Bonehead is already here, and he's jealous of sharing.")
                continue
            player.mana -= 3
            player.raise_skeleton()
            return "done"

        if ans == "4":
            if use_item_menu(player):
                return "done"
            continue   # backed out, show the menu again

        if ans == "5":
            if not enemy.can_flee:
                print(f"{enemy.name} blocks the way. There is no escape!")
                continue
            if random.random() < 0.5:
                print(f"{player.name} gathers her skirts and sprints away!")
                return "fled"
            print("She trips over a root. Flee failed!")
            return "done"


def mortal_kombat(player, enemy):
    """
    Run a full fight. Returns "won", "fled" or "lost".
    """
    print(f"\n{player.name} stands against {enemy.name}. The fight can't be avoided.")

    while player.is_alive() and enemy.is_alive():
        show_hp(player, enemy)

        # --- Player turn ---
        player.idle()
        result = choose_action(player, enemy)
        if result == "fled":
            return "fled"

        # --- Skeleton helper (if any) ---
        if enemy.is_alive():
            player.skeleton_attack(enemy)

        # --- Monster turn ---
        if enemy.is_alive():
            enemy.take_turn(player)

        # --- End of round: tiny mana regeneration ---
        if player.is_alive():
            player.mana = min(player.max_mana, player.mana + 1)

    # The fight is over; clear any leftover skeleton.
    player.minion_turns = 0

    if not player.is_alive():
        print(f"{player.name} is dead. What a sad end.")
        return "lost"

    print(f"\n{enemy.name} is dead. You can move forward.")
    player.gold += enemy.gold_reward
    if enemy.gold_reward:
        print(f"You find {enemy.gold_reward} gold in the remains.")
    player.gain_xp(enemy.xp_reward)
    return "won"


# =============================================================================
# SCENE FUNCTIONS
# Each scene gets the witch and does its thing. They return nothing; the main
# loop checks if the witch is still alive afterwards.
# =============================================================================

def glade01(player):
    print("This is definitely a nice-looking glade.")
    if "glade_seen" not in player.flags:
        player.flags.add("glade_seen")
        print("A butterfly lands on your hat and whispers: 'Grandma's graveyard is east. Mind the dog.'")
        print("Butterflies in the Leet Forest are surprisingly chatty.")


def dark_path(player):
    if "goblin_beaten" in player.flags:
        print("The dark path is quiet now. A confused goblin-shaped dent remains in the moss.")
        return
    print("A wild goblin appears, but is too confused to attack.")
    goblin1 = Monster("Goblin", 3, 8, xp=6, gold=2,
                      idle_call="stares at you, clearly lost.",
                      attack_call="flails its club half-heartedly.")
    if mortal_kombat(player, goblin1) == "won":
        player.flags.add("goblin_beaten")


def stream(player):
    print("Walking along the stream is peaceful.")
    if "nugget_taken" in player.flags:
        print("The stream burbles. You already took the pretty nugget. Greedy witch.")
        return
    print("Oh look, there is a gold nugget among the stones.")
    player.flags.add("nugget_taken")
    player.gold += 5
    print("(+5 gold)")


def mushroom_grove(player):
    print("A ring of chubby mushrooms giggles as you walk in. Each wears a tiny hat.")
    if "mushroom_riddle" in player.flags:
        print("They wave politely. 'Hi again! Still no snacks for us? Fine.'")
        return
    print("'Riddle time!' squeaks the biggest one. 'What do necromancers and bakers share?'")
    print(" 1) they both raise things")
    print(" 2) they both wear aprons")
    print(" 3) nothing, ew")
    ans = ask("> ", ["1", "2", "3"])
    player.flags.add("mushroom_riddle")
    if ans == "1":
        print("The mushrooms cheer! One pops open and hands you a soul tea. (+1 soul tea)")
        player.add_item("soul tea")
    else:
        print("'Wrong, but cute!' The mushrooms toss you a consolation cookie. (+1 moon cookie)")
        player.add_item("moon cookie")


def cat_shop(player):
    print("A wobbly hut on chicken legs. Inside sits a fluffy cat in a tiny apron behind a counter.")
    print("'Meow-welcome. No haggling. I will know.'")

    # The hut is also a safe, cozy rest stop: warm stove, free full heal.
    # (Handy before the boss! The graph lets you walk back here from the bridge.)
    if player.temp_hp < player.max_hp or player.mana < player.max_mana:
        print("You warm your toes by the stove while the cat purrs. HP and MP fully restored.")
        player.temp_hp = player.max_hp
        player.mana = player.max_mana

    # Shop stock: key -> (item name, price)
    stock = {
        "1": ("soul tea", 5),
        "2": ("moon cookie", 4),
        "3": ("ghost pepper jam", 8),
    }
    while True:
        print(f"\nYou have {player.gold} gold.")
        for key, (item, price) in stock.items():
            note = "  <- grandma's favourite!" if item == "ghost pepper jam" else ""
            print(f" {key}) {item} - {price} gold{note}")
        print(" 0) leave")
        ans = ask("> ", ["0", "1", "2", "3"])
        if ans == "0":
            print("'Meow-bye,' says the cat, already napping.")
            return
        item, price = stock[ans]
        if player.gold < price:
            print("The cat stares at your coin purse with deep disappointment.")
            continue
        player.gold -= price
        player.add_item(item)
        print(f"Bought {item}!")


def haunted_orchard(player):
    print("Rows of crooked apple trees. Under them, bones. Many, many cute little bones.")
    if "skeleton" in player.skills:
        print("Bonehead's cousins wave from the grass. You wave back.")
        return
    print("A bone-pile twitches. A tiny skull pops up, wearing a daisy crown.")
    print("'Take me with you, mistress! I can fight for you!'")
    print(" 1) teach the skeleton spell")
    print(" 2) pat the skull and walk on")
    ans = ask("> ", ["1", "2"])
    if ans == "1":
        player.skills.add("skeleton")
        print("You learned RAISE SKELETON! (costs 3 MP, a skeleton fights for 3 turns)")
    else:
        print("The skull sniffles. You feel mildly guilty.")


def swamp(player):
    if "slime_beaten" in player.flags:
        print("The swamp bubbles lazily. Somewhere, a frog judges you.")
        return
    print("Glooop. A big green slime blocks the boardwalk, wearing a lily pad like a hat.")
    slime = Slime("Swamp Slime", 3, 12, xp=10, gold=3,
                  idle_call="wobbles at you menacingly. Mostly cutely.",
                  attack_call="slaps you with a wet pseudopod.")
    if mortal_kombat(player, slime) == "won":
        player.flags.add("slime_beaten")


def troll_bridge(player):
    print("A stone bridge. Under it lives a troll with a clipboard and an eyepatch.")
    if "bridge_open" in player.flags:
        print("The troll nods. 'You're on the list. Move along.'")
        return
    print("'Toll is 6 gold!' he grumbles.")
    print(" 1) pay 6 gold")
    print(" 2) offer a moon cookie")
    print(" 3) fight him")
    ans = ask("> ", ["1", "2", "3"])

    if ans == "1":
        if player.gold >= 6:
            player.gold -= 6
            player.flags.add("bridge_open")
            print("Clink. 'Pleasure doing business.'")
        else:
            print("'Not enough gold!' he scoffs. You're not getting across like this.")
    elif ans == "2":
        if player.use_item("moon cookie"):
            player.flags.add("bridge_open")
            print("The troll tears up. 'Nobody ever offers me cookies.' He lets you through, sniffling.")
        else:
            print("You pat your pockets. No cookie. The troll is unimpressed.")
    else:
        troll = Monster("Bridge Troll", 4, 18, xp=14, gold=6, can_flee=False,
                        idle_call="cracks his knuckles and checks his clipboard.",
                        attack_call="smashes down with a club made of a tree.")
        if mortal_kombat(player, troll) == "won":
            player.flags.add("bridge_open")


def graveyard_gate(player):
    print("The old graveyard gate creaks. Fog curls between the tombstones.")
    if "hound_beaten" in player.flags:
        print("The gate stands open. The dog's ghost snores on a tombstone.")
        return
    print("A huge spectral dog rises up, with a ghostly bone in its mouth.")
    hound = Gloomhound("Gloomhound", 3, 16, xp=20, gold=10, can_flee=False,
                       idle_call="growls, ears flat, tail swishing.",
                       attack_call="snaps its jaws at you.")
    if mortal_kombat(player, hound) == "won":
        player.flags.add("hound_beaten")
        print("The hound whimpers, drops the bone and rolls over for belly scratches. Good ghost dog!")


def grama_grave(player):
    print("You reach your grandmother's grave.")
    print("You place the food on the tombstone.")
    print("Even wicked dead deserve rest.")

    # Two endings, depending on whether you brought the jam.
    if player.has_item("ghost pepper jam"):
        print("\nYou also set down the ghost pepper jam. The air shimmers.")
        print("Grandma's ghost appears in a lacy shawl, spoon already in hand.")
        print("'My favourite! My clever little necromancer!'")
        print("You have tea together until the sun comes up. A tiny skeleton pours.")
        print("THE BEST ENDING: tea, jam and family (mostly dead).")
    else:
        print("\nA soft breeze lifts the basket's cloth. Somewhere, a ghostly voice says:")
        print("'Thank you, dear. Next time bring jam.'")
        print("A sweet ending, but you wonder what the jam would have done.")


# =============================================================================
# SCENE LOOKUP
# Maps a scene name (string stored in a Node) to the function that runs it.
# =============================================================================

scenes = {
    "glade1": glade01,
    "dark_path": dark_path,
    "stream": stream,
    "mushrooms": mushroom_grove,
    "cat_shop": cat_shop,
    "orchard": haunted_orchard,
    "swamp": swamp,
    "bridge": troll_bridge,
    "gate": graveyard_gate,
    "gramma": grama_grave,
}


# =============================================================================
# NAVIGATION
# =============================================================================

class Node:
    """
    One place on the map.
    - nodename: key into the `scenes` dictionary.
    - textto: how this place is described in the "where do you go next" menu.
    - exits: list of other Nodes you can walk to from here.
    (It started as a binary tree, with left and right. Now it's a full graph. Shhh.)
    """

    def __init__(self, nodename, textto=""):
        self.nodename = nodename
        self.textto = textto
        self.exits = []

    def connect(self, other, both_ways=False):
        """Add a path to another node (and optionally back again)."""
        self.exits.append(other)
        if both_ways:
            other.exits.append(self)


# ---- BUILD THE FOREST -------------------------------------------------------

start_node = Node("glade1", "Back to the sunny glade.")
dark = Node("dark_path", "Go down the dark path.")
stream_node = Node("stream", "Follow the stream.")
mushrooms = Node("mushrooms", "Visit the giggling mushroom grove.")
shop = Node("cat_shop", "Follow the smell of fish to the chicken-leg hut.")
orchard = Node("orchard", "Wander into the haunted apple orchard.")
swamp_node = Node("swamp", "Squelch through the swamp boardwalk.")
bridge_node = Node("bridge", "Head for the old stone bridge.")
gate_node = Node("gate", "Approach the foggy graveyard gate.")
end_node = Node("gramma", "You see a familiar tombstone.")

# The glade branches out three ways.
start_node.connect(dark)
start_node.connect(stream_node)
start_node.connect(mushrooms)

# Everything else can be walked in both directions, so the witch can go back
# for tea, jam, or a skeleton. The graph has loops now.
dark.connect(shop, both_ways=True)
stream_node.connect(orchard, both_ways=True)
mushrooms.connect(shop, both_ways=True)
dark.connect(start_node)
stream_node.connect(start_node)
mushrooms.connect(start_node)
orchard.connect(swamp_node, both_ways=True)
shop.connect(bridge_node, both_ways=True)
swamp_node.connect(bridge_node, both_ways=True)
bridge_node.connect(gate_node, both_ways=True)
gate_node.connect(end_node)


def path_choice(now_node):
    """Show the exits of the current node and return the node the player picks."""
    choices = {}
    for i, destination in enumerate(now_node.exits, start=1):
        choices[str(i)] = destination

    print("\nWhere do you go next?")
    for key, destination in choices.items():
        print(f"{key}) {destination.textto}")

    ans = ask("> ", list(choices.keys()))
    return choices[ans]


# =============================================================================
# MAIN LOOP
# =============================================================================

def show_status(witch):
    """A tiny status line shown between scenes, so the player can plan."""
    items = ", ".join(f"{n} x{c}" for n, c in witch.inventory.items() if c > 0) or "nothing"
    print(f"\n[{witch.name} Lv{witch.level} | HP {witch.temp_hp}/{witch.max_hp} | "
          f"MP {witch.mana}/{witch.max_mana} | gold {witch.gold} | items: {items}]")


def main():
    now_node = start_node
    witch = Witch("Morgana", 4, 16)

    print("Little witch enters dark Leet Forest.")
    print("To deliver food basket for her grandma.")
    print("(Grandma is dead, but manners are manners.)")
    print("She sees a spot of light between dark trunks.")

    while True:
        # Load and execute the current scene
        scenes[now_node.nodename](witch)

        if not witch.is_alive():
            print("\nGAME OVER")
            print("The forest gently tucks a leaf blanket over the basket. Try again?")
            break

        # Stop when we reach the grandmother's grave
        if now_node is end_node:
            print("\nYou completed the game!")
            break

        # Between scenes: show status, then choose the next node
        show_status(witch)
        now_node = path_choice(now_node)


if __name__ == "__main__":
    main()
