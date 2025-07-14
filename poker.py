import random
from collections import Counter

# Constants
# Define all suits, ranks, value mappings and hand ranking order
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_values = {rank: i for i, rank in enumerate(ranks, 2)}
hand_ranking = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9
}

#Classes
class Card:
    """A single playing card with suit, rank, and value."""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = rank_values[rank]

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    """A deck of 52 cards that can be shuffled and dealt."""
    def __init__(self):
        self.cards = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(self.cards)

    def deal(self, num):
        """Deal num cards from the deck."""
        return [self.cards.pop() for _ in range(num)]

class Player:
    """Represents a poker player with a name and hand."""
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __str__(self):
        return f"{self.name} Hand: {' '.join(str(card) for card in self.hand)}"

# Hand Evaluation
def evaluate_hand(cards):
    """
    Determine the poker hand rank from 7 cards.
    Returns (hand_type, main_value, kickers)
    """
    values = [card.value for card in cards]
    suits_in_hand = [card.suit for card in cards]
    counts = Counter(values)
    sorted_values = sorted(values, reverse=True)
    unique_values = sorted(set(values), reverse=True)

    # Check for straight (including A-2-3-4-5)
    if 14 in unique_values:
        unique_values.append(1)
    straight = False
    straight_high = 0
    for i in range(len(unique_values) - 4):
        if all(unique_values[i + j] - 1 == unique_values[i + j + 1] for j in range(4)):
            straight = True
            straight_high = unique_values[i]
            break

    # Check for flush (5 cards with same suit)
    flush = False
    flush_suit = ""
    for s in suits_in_hand:
        if suits_in_hand.count(s) >= 5:
            flush = True
            flush_suit = s
            break

    # Check for straight flush
    if flush and straight:
        flush_cards = [card.value for card in cards if card.suit == flush_suit]
        flush_cards = list(set(flush_cards))
        flush_cards.sort(reverse=True)
        if 14 in flush_cards:
            flush_cards.append(1)
        for i in range(len(flush_cards) - 4):
            if all(flush_cards[i + j] - 1 == flush_cards[i + j + 1] for j in range(4)):
                return ("Straight Flush", flush_cards[i], [])

    # Check for four of a kind
    for number in counts:
        if counts[number] == 4:
            kicker = max([v for v in values if v != number])
            return ("Four of a Kind", number, [kicker])

    # Check for full house (three of a kind + a pair)
    three = [num for num, cnt in counts.items() if cnt == 3]
    pairs = [num for num, cnt in counts.items() if cnt == 2]
    if len(three) >= 1:
        if len(three) >= 2:
            return ("Full House", max(three), [min(three)])
        elif len(pairs) >= 1:
            return ("Full House", max(three), [max(pairs)])

    # Check for flush
    if flush:
        top_flush = [card.value for card in cards if card.suit == flush_suit]
        top_flush.sort(reverse=True)
        return ("Flush", top_flush[0], top_flush[1:5])

    # Check for straight
    if straight:
        return ("Straight", straight_high, [])

    # Check for three of a kind
    if len(three) >= 1:
        t = max(three)
        kickers = [v for v in sorted_values if v != t][:2]
        return ("Three of a Kind", t, kickers)

    # Check for two pair
    if len(pairs) >= 2:
        pairs.sort(reverse=True)
        top, second = pairs[0], pairs[1]
        kicker = max([v for v in sorted_values if v != top and v != second])
        return ("Two Pair", top, [second, kicker])

    # Check for one pair
    if len(pairs) == 1:
        pair = pairs[0]
        kickers = [v for v in sorted_values if v != pair][:3]
        return ("One Pair", pair, kickers)

    # Default to high card
    return ("High Card", sorted_values[0], sorted_values[1:5])

# Compare Two Players
def compare_hands(player1, player2, community_cards):
    """
    Compare both players' best hands using their cards and community cards.
    Returns winner's name or "Draw".
    """
    hand1 = player1.hand + community_cards
    hand2 = player2.hand + community_cards
    rank1, val1, kickers1 = evaluate_hand(hand1)
    rank2, val2, kickers2 = evaluate_hand(hand2)

    print(f"\n{player1.name} has: {rank1}")
    print(f"{player2.name} has: {rank2}")

    if hand_ranking[rank1] > hand_ranking[rank2]:
        return player1.name
    elif hand_ranking[rank1] < hand_ranking[rank2]:
        return player2.name
    else:
        if val1 > val2:
            return player1.name
        elif val2 > val1:
            return player2.name
        else:
            for k1, k2 in zip(kickers1, kickers2):
                if k1 > k2:
                    return player1.name
                elif k2 > k1:
                    return player2.name
            return "Draw"

# Main Game Loop
def play_poker_round(name1, name2):
    """
    Play one round: deal cards, show board, and determine winner.
    """
    player1 = Player(name1)
    player2 = Player(name2)
    deck = Deck()
    player1.hand = deck.deal(2)
    player2.hand = deck.deal(2)
    print(f"\n{player1}")
    print(f"{player2}")

    community_cards = []

    input("\nPress Enter to deal the Flop...")
    community_cards += deck.deal(3)
    print("Flop: " + ' '.join(str(card) for card in community_cards))

    input("Press Enter to deal the Turn...")
    community_cards += deck.deal(1)
    print("Turn: " + str(community_cards[3]))

    input("Press Enter to deal the River...")
    community_cards += deck.deal(1)
    print("River: " + str(community_cards[4]))

    print("\nCommunity Cards: " + ' '.join(str(card) for card in community_cards))

    winner = compare_hands(player1, player2, community_cards)

    if winner == "Draw":
        print("\nResult: It's a draw!")
    else:
        print(f"\nResult: {winner} wins!")

def main():
    """Handles user names and controls game rounds."""
    print("Welcome to the Simple Texas Hold'em Poker Game!")
    name1 = input("Enter Player 1 name: ")
    name2 = input("Enter Player 2 name: ")
    while True:
        play_poker_round(name1, name2)
        again = input("\nPlay another round? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
