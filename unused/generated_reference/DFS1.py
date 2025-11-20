from itertools import combinations

def countdown_reachable(numbers):
    reachable = set()
    frontier = [numbers]  # numbers is a tuple

    while frontier:
        current_numbers = frontier.pop()

        # Try all pairs of numbers
        for a, b in combinations(current_numbers, 2):
            # Build the remaining numbers as a tuple
            rest = tuple(x for x in current_numbers if x != a and x != b)

            # Generate all possible results from a and b
            possible_results = set()
            possible_results.add(a + b)
            possible_results.add(a * b)
            possible_results.add(a - b)
            possible_results.add(b - a)
            if b != 0 and a % b == 0:
                possible_results.add(a // b)
            if a != 0 and b % a == 0:
                possible_results.add(b // a)

            # Add numbers in range to reachable and push new states
            for result in possible_results:
                if 100 <= result <= 999:
                    reachable.add(result)
                frontier.append(rest + (result,))

    return reachable

# Example usage:
# numbers = (1, 2, 3, 4, 9, 75)
# reachable_targets = countdown_reachable(numbers)
# print(sorted(reachable_targets))

# BUGGED
if __name__ == "__main__":
    total = 0
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            clean_line = line.strip().replace("{", "").replace("}", "")
            nums = clean_line.strip().split(",")
            initial_state = tuple(int(n) for n in nums)
            reachable_targets = countdown_reachable(initial_state)
            this_sum = len(reachable_targets)
            total += this_sum
            # if idx%100==0:
            print(f"Line {idx} cleared, this line sum is {this_sum}")
    print(total)
    