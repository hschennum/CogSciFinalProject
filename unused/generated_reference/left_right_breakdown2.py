from itertools import combinations

def efficient_countdown(numbers):
    # We'll use tuples of indices as keys, stored in a dictionary
    # Each entry: set of reachable values for that subset
    memo = {}
    
    # Initialize with single numbers
    for i in range(len(numbers)):
        memo[(i,)] = {numbers[i]}
    
    # Frontier: list of subsets we need to process, starting with all single-element subsets
    # We'll process subsets by increasing size
    frontier = []
    for size in range(2, len(numbers) + 1):
        # Generate all subsets of this size
        for indices in combinations(range(len(numbers)), size):
            frontier.append(tuple(sorted(indices)))
    
    # Process the frontier
    for indices in frontier:
        results = set()
        
        # Try all ways to split this subset into two non-empty parts
        # We split by choosing a non-empty proper subset
        for split_size in range(1, len(indices)):
            for left_indices in combinations(indices, split_size):
                left_indices = tuple(sorted(left_indices))
                right_indices = tuple(sorted([i for i in indices if i not in left_indices]))
                
                # Both subsets should be in memo (processed earlier due to smaller size)
                for left_val in memo[left_indices]:
                    for right_val in memo[right_indices]:
                        # Addition
                        results.add(left_val + right_val)
                        # Multiplication
                        results.add(left_val * right_val)
                        # Subtraction (positive results only)
                        if left_val > right_val:
                            results.add(left_val - right_val)
                        if right_val > left_val:
                            results.add(right_val - left_val)
                        # Division (exact division only)
                        if right_val != 0 and left_val % right_val == 0:
                            results.add(left_val // right_val)
                        if left_val != 0 and right_val % left_val == 0:
                            results.add(right_val // left_val)
        
        memo[indices] = results
    
    # Get results for the full set
    full_set = tuple(range(len(numbers)))
    all_results = memo[full_set]
    
    # Filter positive integers
    positive_ints = {x for x in all_results if x > 0 and isinstance(x, int)}
    return sorted(positive_ints)

# Test with our specific set
numbers = [1, 2, 3, 4, 9, 75]
reachable = efficient_countdown(numbers)
targets = [x for x in reachable if 100 <= x <= 999]

print(f"With numbers {numbers}:")
print(f"Total reachable numbers: {len(reachable)}")
print(f"Reachable targets in 100-999: {len(targets)}")

# BUGGED
if __name__ == "__main__":
    total = 0
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            clean_line = line.strip().replace("{", "").replace("}", "")
            nums = clean_line.strip().split(",")
            initial_state = list(int(n) for n in nums)
            reachable_targets = efficient_countdown(initial_state)
            reachable_targets = [x for x in reachable_targets if 100 <= x <= 999]
            this_sum = len(reachable_targets)
            total += this_sum
            # if idx%100==0:
            print(f"Line {idx} cleared, this line sum is {this_sum}")
    print(total)