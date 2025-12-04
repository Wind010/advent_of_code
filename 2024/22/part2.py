'''
https://adventofcode.com/2024/day/22
'''


from functools import cache
from itertools import product
import re
from common.common import arg_parse, assertions, timer
from part1 import next_secret
from multiprocessing import Pool


def simulate_prices(initial_secret, iterations=2000):
    """Simulates the prices derived from the secret number sequence."""
    secret = initial_secret
    MODULO = 16777216
    prices = []

    for _ in range(iterations + 1):  # +1 to include the initial price
        prices.append(secret % 10)  # Price is the last digit of the secret number

        # Step 1: Multiply by 64, mix, prune
        secret ^= (secret * 64) % MODULO
        secret %= MODULO

        # Step 2: Divide by 32, round down, mix, prune
        secret ^= (secret // 32) % MODULO
        secret %= MODULO

        # Step 3: Multiply by 2048, mix, prune
        secret ^= (secret * 2048) % MODULO
        secret %= MODULO

    return prices


def precompute_price_changes(prices):
    """Precomputes the price changes for a given list of prices."""
    return [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]


def find_sequence_bananas(prices, price_changes, sequence):
    """Calculates the bananas collected from a sequence for a buyer."""
    seq_len = len(sequence)
    for i in range(len(price_changes) - seq_len + 1):
        if price_changes[i:i + seq_len] == sequence:
            # Return the price at the index where the sequence ends
            return prices[i + seq_len]
    return 0


def evaluate_sequence(sequence, buyer_data):
    """Evaluates the total bananas for a given sequence across all buyers."""
    total_bananas = 0
    for prices, changes in buyer_data:
        total_bananas += find_sequence_bananas(prices, changes, sequence)
    return total_bananas


def find_best_sequence(initial_secrets):
    """Finds the best sequence of 4 price changes that maximizes bananas."""
    # Simulate prices and precompute changes for all buyers
    buyer_data = [
        (prices := simulate_prices(secret), precompute_price_changes(prices))
        for secret in initial_secrets
    ]

    # Generate all possible sequences of 4 price changes
    all_sequences = list(product(range(-9, 10), repeat=4))

    max_bananas = 0
    best_sequence = None

    # Use multiprocessing to speed up evaluation
    with Pool() as pool:
        results = pool.starmap(
            evaluate_sequence,
            [(sequence, buyer_data) for sequence in all_sequences]
        )

    for seq, bananas in zip(all_sequences, results):
        if bananas > max_bananas:
            max_bananas = bananas
            best_sequence = seq

    return best_sequence, max_bananas






def main(args, data):
    lines = data.strip().split('\n')
    initial_secrets = [*map(int, lines)]
    
    best_sequence, max_bananas = find_best_sequence(initial_secrets)
    
    assertions(args, max_bananas, 23, 9, 9)
    return max_bananas
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

