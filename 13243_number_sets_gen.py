# Hayden Schennum
# 2025-11-18

import itertools

small_numbers = list(range(1, 11))
large_numbers = [25, 50, 75, 100]
all_numbers = small_numbers + large_numbers  # all 14 distinct numbers

with open("13243_number_sets.txt", "w") as fh:
    # Case 1: No pairs (6 distinct numbers)
    for combo in itertools.combinations(all_numbers, 6): # 14C6
        line = sorted(combo)
        fh.write(",".join(map(str, line)) + "\n")
    
    # Case 2: One pair (exactly one repeated small number)
    for pair_num in small_numbers: # 10C1 pair nums possible
        remaining_nums = [n for n in all_numbers if n != pair_num] # 13 remaining nums
        for combo in itertools.combinations(remaining_nums, 4): # 13C4
            line = sorted([pair_num, pair_num] + list(combo))
            fh.write(",".join(map(str, line)) + "\n")
    
    # Case 3: Two pairs (exactly two repeated small numbers)
    for pair_nums in itertools.combinations(small_numbers, 2): # 10C2 two-pairs possible 
        remaining_nums = [n for n in all_numbers if n not in pair_nums] # 12 remaining nums
        for combo in itertools.combinations(remaining_nums, 2): # 12C2
            line = sorted([pair_nums[0], pair_nums[0], pair_nums[1], pair_nums[1]] + list(combo))
            fh.write(",".join(map(str, line)) + "\n")
    
    # Case 4: Three pairs (exactly three repeated small numbers)
    for pair_nums in itertools.combinations(small_numbers, 3): # 10C3 three-pairs possible
        line = sorted([pair_nums[0], pair_nums[0], pair_nums[1], pair_nums[1], pair_nums[2], pair_nums[2]])
        fh.write(",".join(map(str, line)) + "\n")

print("All sets written")

