from collections import deque

def optimized_countdown_dfs(numbers):
    reachable = set()
    stack = deque([(set(numbers), [])])  # (available_numbers, operations_history)
    visited = set()
    
    while stack:
        available, history = stack.pop()
        state_key = tuple(sorted(available))
        
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Add all current numbers to reachable if in range
        for num in available:
            if 100 <= num <= 999:
                reachable.add(num)
        
        # Try all pairs and operations
        available_list = list(available)
        for i in range(len(available_list)):
            for j in range(i + 1, len(available_list)):
                a, b = available_list[i], available_list[j]
                
                # Generate all possible operations
                operations = []
                operations.append(('+', a + b))
                if a > b:
                    operations.append(('-', a - b))
                elif b > a:
                    operations.append(('-', b - a))
                operations.append(('*', a * b))
                if b != 0 and a % b == 0:
                    operations.append(('/', a // b))
                if a != 0 and b % a == 0:
                    operations.append(('/', b // a))
                
                for op, result in operations:
                    if result <= 0:  # Only positive integers
                        continue
                    
                    # Create new set without a and b, but with result
                    new_available = set(available)
                    new_available.remove(a)
                    new_available.remove(b)
                    new_available.add(result)
                    
                    stack.append((new_available, history + [(a, op, b, result)]))
    
    return reachable

# Run the optimized version
numbers = [1, 2, 5, 7, 75, 100]
reachable = optimized_countdown_dfs(numbers)
targets_in_range = [num for num in reachable if 100 <= num <= 999]
targets_in_range.sort()

print(f"Total reachable targets in range 100-999: {len(targets_in_range)}")
print(f"Reachable targets: {targets_in_range}")

# BUGGED
if __name__ == "__main__":
    total = 0
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            clean_line = line.strip().replace("{", "").replace("}", "")
            nums = clean_line.strip().split(",")
            initial_state = list(int(n) for n in nums)
            reachable_targets = optimized_countdown_dfs(initial_state)
            reachable_targets = [num for num in reachable_targets if 100 <= num <= 999]
            this_sum = len(reachable_targets)
            total += this_sum
            # if idx%100==0:
            print(f"Line {idx} cleared, this line sum is {this_sum}")
    print(total)