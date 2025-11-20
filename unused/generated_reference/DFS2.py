from collections import deque

def countdown_dfs(numbers):
    # We'll use BFS/DFS with a queue/stack to process states
    # Each state is a set of available numbers
    # We'll track all reachable numbers
    reachable = set()
    
    # Use a stack for DFS
    stack = deque()
    
    # Start with all numbers available
    initial_state = tuple(sorted(numbers))
    stack.append(initial_state)
    visited = set()
    visited.add(initial_state)
    
    while stack:
        current_state = stack.pop()
        current_numbers = list(current_state)
        
        # Add all current numbers to reachable
        for num in current_numbers:
            if 100 <= num <= 999:
                reachable.add(num)
        
        # If we have only one number, we can't combine further
        if len(current_numbers) == 1:
            continue
            
        # Try all pairs of numbers
        for i in range(len(current_numbers)):
            for j in range(i + 1, len(current_numbers)):
                a, b = current_numbers[i], current_numbers[j]
                
                # Generate new numbers from a and b
                new_numbers = []
                
                # Addition
                new_numbers.append(a + b)
                
                # Subtraction (positive results only)
                if a > b:
                    new_numbers.append(a - b)
                elif b > a:
                    new_numbers.append(b - a)
                
                # Multiplication
                new_numbers.append(a * b)
                
                # Division (integer results only)
                if b != 0 and a % b == 0:
                    new_numbers.append(a // b)
                if a != 0 and b % a == 0:
                    new_numbers.append(b // a)
                
                # Create new state for each valid operation result
                for new_num in new_numbers:
                    if new_num <= 0:  # Only positive integers
                        continue
                        
                    # Create new set of numbers
                    remaining_numbers = []
                    for k in range(len(current_numbers)):
                        if k != i and k != j:
                            remaining_numbers.append(current_numbers[k])
                    remaining_numbers.append(new_num)
                    
                    new_state = tuple(sorted(remaining_numbers))
                    
                    if new_state not in visited:
                        visited.add(new_state)
                        stack.append(new_state)
    
    return reachable

# Test with the given numbers
numbers = [1, 2, 5, 7, 75, 100]
reachable = countdown_dfs(numbers)

# Filter for targets in range 100-999
targets_in_range = [num for num in reachable if 100 <= num <= 999]
targets_in_range.sort()

print(f"Total reachable targets in range 100-999: {len(targets_in_range)}")

# NOT BUGGED - this one passed with totals
# 1226_perfect_sets.txt -> should be 1103400 solvable
# 13243_number_sets.txt -> should be 10871986 solvable
if __name__ == "__main__":
    total = 0
    with open("13243_number_sets.txt", "r") as fh:
    # with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            clean_line = line.strip().replace("{", "").replace("}", "")
            nums = clean_line.strip().split(",")
            initial_state = list(int(n) for n in nums)
            reachable_targets = countdown_dfs(initial_state)
            reachable_targets = [num for num in reachable_targets if 100 <= num <= 999]
            this_sum = len(reachable_targets)
            total += this_sum
            if idx%100==0:
                print(f"Line {idx} cleared, this line sum is {this_sum}")
    print(total)
    