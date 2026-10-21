"""
ART GALLERY GAME

Run an art gallery, bid against a computer-controlled art accumulator, and curate
an exhibition that attracts visitors. Matching artists, styles, and themes boosts
your gallery's appeal. Earn money from ticket sales to buy more art.

The game ends after the auction deck is empty and the player sells tickets.
"""

import random
from collections import Counter
from dataclasses import dataclass, field


PAINTINGS = [
    "Mona Lisa",
    "The Starry Night",
    "The Scream",
    "Girl with a Pearl Earring",
    "The Last Supper",
    "Guernica",
    "The Persistence of Memory",
    "The Birth of Venus",
    "The Kiss",
    "American Gothic",
    "The Night Watch",
    "The Great Wave off Kanagawa",
    "Las Meninas",
    "The Creation of Adam",
    "Water Lilies",
    "The Garden of Earthly Delights",
    "Liberty Leading the People",
    "A Sunday Afternoon on the Island of La Grande Jatte",
    "The Arnolfini Portrait",
    "Whistler's Mother",
]

ARTISTS = [
    "Da Vinci", "Van Gogh", "Picasso", "Monet", "Rembrandt",
    "Michelangelo", "Klimt", "Dali", "Vermeer", "Munch",
]

STYLES = [
    "Renaissance", "Baroque", "Impressionism", "Post-Impressionism",
    "Cubism", "Surrealism", "Expressionism", "Realism",
    "Romanticism", "Abstract",
]

THEMES = [
    "Portrait", "Landscape", "Seascape", "Still Life", "Mythology",
    "Religion", "War", "Love", "Nature", "Everyday Life",
]


@dataclass(eq=False)
class Painting:
    name: str
    artist: str
    style: str
    theme: str
    quality: int = field(default_factory=lambda: random.randint(1, 10))

    @property
    def price(self) -> int:
        return 50 + 10 * self.quality

    def display(self) -> str:
        return f"{self.name} by {self.artist}"

    def display_long(self) -> str:
        return (
            f"{self.name} by {self.artist} — "
            f"{self.style} style, theme: {self.theme}"
        )

    def market_value(self) -> str:
        return f"Quality: {self.quality}/10 | Market value: ${self.price}"


@dataclass
class Gallery:
    name: str
    cash: int
    ticket_price: int = 3
    exhibit: list[Painting] = field(default_factory=list)
    storage: list[Painting] = field(default_factory=list)
    appeal: int = 0
    visitors: int = 0
    visitors_total: int = 0
    

    MAX_EXHIBIT_SIZE = 5

    def to_storage(self, painting: Painting) -> None:
        if painting not in self.storage and painting not in self.exhibit:
            self.storage.append(painting)

    def to_exhibit(self, painting: Painting) -> bool:
        if painting not in self.storage:
            print("That painting is not in your storage.")
            return False
        if len(self.exhibit) >= self.MAX_EXHIBIT_SIZE:
            print("Your exhibition is full. Move a painting to storage first.")
            return False

        self.storage.remove(painting)
        self.exhibit.append(painting)
        return True

    def out_exhibit(self, painting: Painting) -> bool:
        if painting not in self.exhibit:
            print("That painting is not in your exhibition.")
            return False

        self.exhibit.remove(painting)
        self.storage.append(painting)
        return True

    def show_exhibition(self) -> None:
        if not self.exhibit:
            print("Your exhibition is empty.")
            return
        for index, painting in enumerate(self.exhibit, start=1):
            print(f"{index}. {painting.display_long()}")

    def evaluate(self) -> int:
        """Calculate exhibition appeal from quality and matching tags."""
        if not self.exhibit:
            self.appeal = 0
            return self.appeal

        total_quality = sum(painting.quality for painting in self.exhibit)
        tags = Counter(
            tag
            for painting in self.exhibit
            for tag in (painting.artist, painting.style, painting.theme)
        )

        multiplier = 1
        for count in tags.values():
            if count == 5:
                multiplier += 3
            elif count == 4:
                multiplier += 2
            elif count == 3:
                multiplier += 1

        # Reward a new combination of paintings only once per game.
        combination = frozenset(p.name for p in self.exhibit)
        if combination not in novelty_combinations:
            multiplier += 3
            #novelty_combinations.add(combination)

        self.appeal = total_quality * multiplier
        self.visitors = self.appeal
        return self.appeal

    def sell_art(self, buyer: "Gallery", painting: Painting, multiplier: float = 1.0) -> bool:
        price = round(painting.price * multiplier)

        if painting not in self.storage:
            print("The painting must be in the seller's storage.")
            return False
        if buyer is self:
            print("You cannot sell a painting to yourself.")
            return False
        if buyer.cash < price:
            print(f"{buyer.name} cannot afford it. The price is ${price}.")
            return False

        self.storage.remove(painting)
        buyer.storage.append(painting)
        buyer.cash -= price
        self.cash += price
        print(f"Sold {painting.name} to {buyer.name} for ${price}.")
        return True

    def earn_ticket_revenue(self) -> int:
        revenue = self.appeal * self.ticket_price
        self.cash += revenue
        self.visitors_total += self.visitors # we compare total visitors over all turns
        print(
            f"{self.name} attracted {self.appeal} visitors "
            f"and earned ${revenue} from ticket sales."
        )
        combination = frozenset(p.name for p in self.exhibit)
        novelty_combinations.add(combination)
        return revenue

    def evaluate_competitor(self) -> int:
        """The computer's strategy is to accumulate art rather than curate it.
Computer does not build exhbitions, just vomits art like city hall museum, but can show even 20 art at once. """
        self.appeal = sum(painting.quality for painting in self.storage+self.exhibit)
        self.visitors = self.appeal
        return self.appeal


novelty_combinations: set[frozenset[str]] = set()


def make_art_deck() -> list[Painting]:
    names = PAINTINGS.copy()
    random.shuffle(names)
    deck = []
    for name in names:
        deck.append(
            Painting(
                name=name,
                artist=random.choice(ARTISTS),
                style=random.choice(STYLES),
                theme=random.choice(THEMES),
            )
        )
    return deck


def choose_index(prompt: str, upper_bound: int) -> int | None:
    """Ask for a 1-based list index; return None to cancel."""
    if upper_bound == 0:
        print("There are no paintings to choose from.")
        return None

    while True:
        answer = input(prompt).strip().lower()
        if answer in {"q", "b", "back"}:
            return None
        try:
            index = int(answer)
        except ValueError:
            print("Enter a number, or type 'b' to go back.")
            continue
        if 1 <= index <= upper_bound:
            return index - 1
        print(f"Choose a number from 1 to {upper_bound}.")


def auction(deck: list[Painting], player: Gallery, competitor: Gallery) -> None:
    if not deck:
        print("There are no paintings left in the auction.")
        return

    painting = deck.pop()
    bid = 50
    if player.cash < 50 and competitor.cash < 50:
    print("Neither gallery can afford the opening bid.")
    deck.append(painting)
    return
    
    if competitor.cash>=50:
        current_bidder = competitor
    else:
        current_bidder=None

    print("\nPainting up for auction:")
    print(painting.display_long())
    print(painting.market_value())
    print(f"Opening bid: ${bid}. {competitor.name} currently holds the bid.")

    while True:
        next_bid = bid + 10
        if player.cash < next_bid:
            print("You cannot afford the next bid.")
            winner = current_bidder
            break

        answer = input(f"Current bid: ${bid}. Bid ${next_bid}? (y/n): ").strip().lower()
        if answer not in {"y", "n"}:
            print("Please enter 'y' or 'n'.")
            continue
        if answer == "n":
            winner = current_bidder
            break

        bid = next_bid
        current_bidder = player
        print(f"You raise the bid to ${bid}.")

        next_bid = bid + 10
        if competitor.cash < next_bid:
            print(f"{competitor.name} cannot afford the next bid.")
            winner = player
            break

        resign_chance = 75 if bid > painting.price else 25
        if random.randint(1, 100) <= resign_chance:
            print(f"{competitor.name} gives up.")
            winner = player
            break

        bid = next_bid
        current_bidder = competitor
        print(f"{competitor.name} raises the bid to ${bid}.")

    
    if winner is None:
        print("Nobody can afford the painting. It returns to the deck.")
        deck.append(painting)
        return
    elif  winner.cash < bid:
        # This should rarely occur, but keeps settlement safe if bids are changed.
        print("The winning bidder cannot cover the final bid. The painting returns to the deck.")
        deck.append(painting)
        return

    winner.storage.append(painting)
    winner.cash -= bid
    print(f"{winner.name} wins {painting.name} for ${bid}.")


def list_paintings(title: str, paintings: list[Painting], show_value: bool = False) -> None:
    print(f"\n{title}")
    if not paintings:
        print("  (empty)")
        return
    for index, painting in enumerate(paintings, start=1):
        print(f"{index}. {painting.display_long()}")
        if show_value:
            print(f"   {painting.market_value()}")


def manage_exhibition(player: Gallery) -> None:
    while True:
        list_paintings("Your exhibition:", player.exhibit)
        print("\n1) Move a painting to storage\n2) Back to menu")
        choice = input("> ").strip()
        if choice == "2":
            return
        if choice != "1":
            print("Choose 1 or 2.")
            continue
        index = choose_index("Which painting? (or b to go back): ", len(player.exhibit))
        if index is not None:
            player.out_exhibit(player.exhibit[index])


def manage_storage(player: Gallery, competitor: Gallery) -> None:
    while True:
        list_paintings("Your storage:", player.storage, show_value=True)
        print("\n1) Move painting to exhibition\n2) Sell painting to competitor")
        print("3) Back to menu")
        choice = input("> ").strip()

        if choice == "3":
            return
        if choice not in {"1", "2"}:
            print("Choose 1, 2, or 3.")
            continue

        index = choose_index("Which painting? (or b to go back): ", len(player.storage))
        if index is None:
            continue
        painting = player.storage[index]

        if choice == "1":
            player.to_exhibit(painting)
        else:
            player.sell_art(competitor, painting)


def manage_competitor_storage(player: Gallery, competitor: Gallery) -> None:
    while True:
        list_paintings(f"{competitor.name}'s storage:", competitor.storage, show_value=True)
        print("\n1) Buy a painting (twice market value)\n2) Back to menu")
        choice = input("> ").strip()
        if choice == "2":
            return
        if choice != "1":
            print("Choose 1 or 2.")
            continue

        index = choose_index("Which painting? (or b to go back): ", len(competitor.storage))
        if index is None:
            continue
        competitor.sell_art(player, competitor.storage[index], multiplier=2.0)


def sell_tickets(player: Gallery, competitor: Gallery, deck: list[Painting]) -> bool:
    print("\nOpening day!")
    player.evaluate()
    competitor.evaluate_competitor()
    player.earn_ticket_revenue()
    competitor.earn_ticket_revenue()

    if not deck:
        final_end(player, competitor)
        return True
    return False


def change_name(player: Gallery) -> None:
    print(f"Your gallery is currently called '{player.name}'.")
    if input("Change the name? (y/n): ").strip().lower() != "y":
        return
    while True:
        name = input("Enter a new gallery name: ").strip()
        if name:
            player.name = name
            print(f"Your gallery is now called '{player.name}'.")
            return
        print("The name cannot be empty.")


def final_end(player: Gallery, competitor: Gallery) -> None:
    print("\n=== GAME OVER ===")
    print(f"Your visitors: {player.visitors_total}")
    print(f"Competitor visitors: {competitor.visitors_total}")
    if player.visitors_total > competitor.visitors_total:
        print("You win! Your curated exhibition attracted more visitors.")
    elif player.visitors_total < competitor.visitors_total:
        print("The computer wins. Better luck next time!")
    else:
        print("It's a draw!")


def menu(player: Gallery, competitor: Gallery, deck: list[Painting]) -> bool:
    print(f"\n=== {player.name} ===")
    print(f"Cash: ${player.cash} | Visitors last opening: {player.visitors}")
    print(f"Paintings left to auction: {len(deck)}")
    print("1) Sell tickets / open gallery")
    print("2) Auction house")
    print("3) Manage exhibition")
    print("4) Manage storage")
    print("5) Browse competitor's storage")
    print("6) Change gallery name")
    print("7) Quit game")

    choice = input("Choose 1-7: ").strip()
    if choice == "1":
        return sell_tickets(player, competitor, deck)
    if choice == "2":
        auction(deck, player, competitor)
    elif choice == "3":
        manage_exhibition(player)
    elif choice == "4":
        manage_storage(player, competitor)
    elif choice == "5":
        manage_competitor_storage(player, competitor)
    elif choice == "6":
        change_name(player)
    elif choice == "7":
        print("Thanks for playing. Running an art gallery is a full-time job!")
        return True
    else:
        print("Please choose a number from 1 to 7.")
    return False


def main() -> None:
    deck = make_art_deck()
    player = Gallery("Midnight Showtime", 500)
    competitor = Gallery("Bob's Accumulation", 1000)

    print("Welcome to Art Gallery Game!")
    print("Curate an exhibition of up to five paintings and attract more visitors than your rival.")
    print("Tip: matching artists, styles, or themes can increase your exhibition's appeal.")

    while True:
        if menu(player, competitor, deck):
            break


if __name__ == "__main__":
    main()

