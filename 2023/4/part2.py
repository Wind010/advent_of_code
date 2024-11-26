'''
--- Day 4: Scratchcards ---
--- Part Two ---
Just as you're about to report your findings to the Elf, one of you realizes that the rules have actually been printed on the back of every card this whole time.

There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)

This time, the above example goes differently:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
Your copy of card 2 also wins one copy each of cards 3 and 4.
Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?
'''


import re
from common.common import arg_parse

def get_cards(lines):
    pattern = r"Card\s+(\d+):\s+([\d\s]+)\s*\|\s*([\d\s]+)"
    cards = {i: 1 for i in range(1, len(lines)+1)}  # Need to predefine the key and value for reference later.  Start off with 1.
    for line in lines:
        match = re.match(pattern, line)
        if match:
            # Extract the two sets of numbers
            card_number = int(match.group(1))  # Or just enumerate lines
            winning_string = match.group(2)
            player_string = match.group(3)
            #print(winning_string, player_string)
            
            winning_set, player_set = set([int(n) for n in winning_string.split()]), set([int(n) for n in player_string.split()])
            winning_numbers = winning_set.intersection(player_set)
            
            for c in range(len(winning_numbers)):
                copy = card_number + c + 1
                cards[copy] += cards[card_number]  # Update the existing count.
            
            #print(winning_numbers)
        else:
            print("☹️:" + line)

    return cards


def get_cards_2(lines):
    cards = {i: 1 for i in range(1, len(lines)+1)} 
    for i, line in enumerate(lines, 1):
        parts = [s for s in line.split(" ") if s != ""]
        sep = parts.index("|")

        wins = list(map(int, parts[2:sep]))
        player = list(map(int, parts[sep + 1:]))

        score = 0
        for v in player:
            if v in wins:
                score += 1

        for j in range(i + 1, i + score + 1):
            cards[j] += cards[i]

    return cards



def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
 
    cards = get_cards(lines)
    cards2 = get_cards_2(lines)
    
    #assert cards == cards2
    
    total_sum = sum(cards.values())
            
    if 'input1.txt' in file_path: assert total_sum == 30
    if 'input2.txt' in file_path: assert total_sum == 6857330 

    print(total_sum)
    return total_sum
            

            
            

if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
