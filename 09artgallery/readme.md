# 🎨 Art Gallery Game

A small Python console game about running an art gallery. Bid against a
computer-controlled rival — **Bob's Accumulation** — and curate an exhibition
that attracts more visitors than his ever-growing pile of art.

## How it works

- Each round, one painting goes up for **auction** (20 famous paintings total,
  with randomized artist, style, theme, and quality).
- Bid against the computer. Bids start at $50 and rise in $10 steps. The
  computer is more likely to give up once the bid exceeds the painting's
  market value.
- Build an **exhibition** of up to 5 paintings. Total quality drives your
  appeal, and **matching artists, styles, or themes** (3, 4, or 5 of a kind)
  multiply it. Showing a brand-new combination of paintings gives a one-time
  novelty bonus.
- **Sell tickets** to earn revenue (appeal × ticket price) and end the round.
- You can also buy paintings from your rival at twice market value, or sell
  him yours at market value.

## Game loop

1. Sell tickets / open gallery
2. Auction house
3. Manage exhibition
4. Manage storage
5. Browse competitor's storage
6. Change gallery name
7. Quit game

## Ending

The game ends when the auction deck is empty and you sell tickets. The gallery
with the **most total visitors** across all openings wins.

- You start with **$500**.
- Bob starts with **$1000** — but he just hoards art instead of curating it.

## Running

Requires Python 3.10+ (uses `dataclass` and `list[...]` type hints).

```bash
python art_gallery_game.py
```
