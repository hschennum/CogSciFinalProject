from itertools import combinations

def optimized_countdown_no_cache(numbers):
    """Compute reachable numbers without bitwise operations or lru_cache."""
    
    # Dictionary to store already computed subsets
    reached = {}

    # tuple<int> -> set<int>
    def compute_reachable(subset):
        # Sort subset to have consistent keys
        key = tuple(sorted(subset))
        if key in reached:
            return reached[key]

        if len(subset) == 1:
            reached[key] = {subset[0]}
            return reached[key]

        reachable = set()
        # Split subset into two non-empty parts
        for i in range(1, len(subset)):
            for left_indices in combinations(range(len(subset)), i):
                left = tuple(subset[j] for j in left_indices)
                right = tuple(subset[j] for j in range(len(subset)) if j not in left_indices)

                for a in compute_reachable(left):
                    for b in compute_reachable(right):
                        reachable.add(a + b)
                        reachable.add(a * b)
                        if a > b:
                            reachable.add(a - b)
                        elif b > a:
                            reachable.add(b - a)
                        if b != 0 and a % b == 0:
                            reachable.add(a // b)
                        if a != 0 and b % a == 0:
                            reachable.add(b // a)

        reached[key] = reachable
        return reachable

    # Compute all reachable numbers for the full set
    reachable_all = compute_reachable(tuple(numbers))

    # Filter to numbers in 100–999
    reachable_targets = {num for num in reachable_all if 100 <= num <= 999}
    return reachable_targets


# Example usage
numbers = [1, 2, 3, 4, 9, 75]
reachable = optimized_countdown_no_cache(numbers)

print(f"Reachable targets (100-999): {len(reachable)}")
# print(f"First 30 reachable: {sorted(reachable)[:30]}")

# BUGGED
if __name__ == "__main__":
    total = 0
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            clean_line = line.strip().replace("{", "").replace("}", "")
            nums = clean_line.strip().split(",")
            initial_state = list(int(n) for n in nums)
            reachable_targets = optimized_countdown_no_cache(initial_state)
            this_sum = len(reachable_targets)
            total += this_sum
            # if idx%100==0:
            print(f"Line {idx} cleared, this line sum is {this_sum}")
    print(total)