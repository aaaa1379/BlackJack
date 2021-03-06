# Play
```python
game.py -h             # see help
game.py -r <round>     # game rounds
```

# Play with Strategy
```python
game.py -s <strategy>
game.py -s easyAction
game.py -r 3 -s easyAction
game.py -r 3 -s basicStrategy
```

# Schedule
## Completed
1. shuffling Machine
1. Card Counting
1. Player
  - Decisions
  - Bet
  - Insurance
1. Dealer
1. Basic Strategy
1. Kelly Criterion

## Todo
1. Rules
1. Player
  - Insurance

# Rules
## Number of Decks
## Soft 17
- `H17` - Dealer Hits on soft 17
- `S17` - Dealer Htands on soft 17

## Permitted Doubles
- `DOA` - Double On Any 2 Cards
- Double On 9/10/11 only (Reno)
- Double On 10/11 only (Reno)

## Double After Split
- `DAS` - Double After Split
- No Double After Split

## Resplit
- Resplit to 4
- Unlimited Resplit

## Surrender
- Early Surrender (rare)
- Late Surrender
- No Surrender

# Reference
- [BlackJack Wiki](https://en.wikipedia.org/wiki/Blackjack#Rules_of_play_at_casinos)
- [Card Counting](https://en.wikipedia.org/wiki/Card_counting)
- [Basic Strategy](https://www.blackjackinfo.com/blackjack-basic-strategy-engine/?numdecks=8&soft17=h17&dbl=all&das=yes&surr=es&peek=yes)
- [Blackjack Games](http://wizardofodds.com/play/blackjack/)
- [Kelly Criterion](https://en.wikipedia.org/wiki/Kelly_criterion)
