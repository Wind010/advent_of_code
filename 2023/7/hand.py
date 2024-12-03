from collections import Counter


FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIRS = 3
ONE_PAIR = 2
HIGH_CARD = 1


class Hand:
    
    def __init__(self, cards):
        self.cards = list(cards)
        self.card_set = set(cards)
        self.card_counts = Counter(cards)
        self.value = self.get_value()
        self.numeric_values = NUMERIC_VALUES
        
    def is_five_of_a_kind(self):
        return len(self.card_set) == 1
    
    def is_four_of_a_kind(self):
        if len(self.card_set) != 2:
            return False
        return any(c for c in self.card_counts.values() if c == 4)
    
    def is_full_house(self):
        has_triplet = any(c for c in self.card_counts.values() if c == 3)
        has_pair = any(c for c in self.card_counts.values() if c == 2)
        return has_triplet and has_pair
    
    def is_three_of_a_kind(self):
        return any(c for c in self.card_counts.values() if c == 3)
    
    def is_two_pairs(self):
        pairs = [c for c in self.card_counts.values() if c == 2]
        return len(pairs) == 2
    
    def is_one_pair(self):
        pairs = [c for c in self.card_counts.values() if c == 2]
        return len(pairs) == 1
        
    def get_value(self):
        if self.is_five_of_a_kind():
            return FIVE_OF_A_KIND
        if self.is_four_of_a_kind():
            return FOUR_OF_A_KIND
        if self.is_full_house():
            return FULL_HOUSE
        if self.is_three_of_a_kind():
            return THREE_OF_A_KIND
        if self.is_two_pairs():
            return TWO_PAIRS
        if self.is_one_pair():
            return ONE_PAIR
        
        return HIGH_CARD
    
    def __lt__(self, other):
        if self.value.value != other.value.value:
            return self.value.value < other.value.value
        else:
            for c1, c2 in zip(self.cards, other.cards):
                c1_value = self.numeric_values[c1]
                c2_value = self.numeric_values[c2]
                if c1_value == c2_value:
                    continue
                return c1_value < c2_value
    
    def __repr__(self):
        return f'<Hand: {"".join(self.cards)} {self.value}>'