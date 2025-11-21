from collections import deque
import time

def countdown_dfs(numbers):

    reachable = set()
    visited = set()
    frontier = deque() # LIFO queue (stack)
    
    # frontier.append(numbers)
    # initial_key = tuple(sorted(numbers))
    # visited.add(initial_key)
    initial_state = tuple(sorted(numbers))
    frontier.append(initial_state)
    visited.add(initial_state)
    
    while len(frontier) > 0:
        current_state = frontier.pop()
        current_numbers = list(current_state)
        
        for num in current_numbers:
            if 100 <= num <= 999:
                reachable.add(num)
        
        if len(current_numbers) == 1:
            continue
            
        for i in range(len(current_numbers)):
            for j in range(i + 1, len(current_numbers)):
                a, b = current_numbers[i], current_numbers[j]
                
                if a > b:
                    a,b = b,a # so b >= a in the following
 
                new_numbers = [b + a]
                if b > a:
                    new_numbers.append(b - a)
                new_numbers.append(b * a)
                if b % a == 0:
                    new_numbers.append(b // a)
                
                for new_num in new_numbers:
                    remaining_numbers = deque()
                    for k in range(len(current_numbers)):
                        if k != i and k != j:
                            remaining_numbers.append(current_numbers[k])
                    remaining_numbers.appendleft(new_num)
                    
                    # new_key = tuple(sorted(remaining_numbers))
                    # new_state = tuple(remaining_numbers)
                    # if new_key not in visited:
                    #     visited.add(new_key)
                    #     frontier.append(new_state)
                    new_state = tuple(sorted(remaining_numbers))
                    if new_state not in visited:
                        visited.add(new_state)
                        frontier.append(new_state)
    
    return reachable

# Test with the given numbers
numbers = (100, 1, 2, 5, 7, 75)
reachable = countdown_dfs(numbers)

# Filter for targets in range 100-999
targets_in_range = [num for num in reachable if 100 <= num <= 999]
targets_in_range.sort()

print(f"Total reachable targets in range 100-999: {len(targets_in_range)}")

# NOT BUGGED - this one passed with totals
# 1226_perfect_sets.txt -> should be 1103400 solvable
# 13243_number_sets.txt -> should be 10871986 solvable
if __name__ == "__main__":
    start_time = time.time()
    total = 0
    # with open("13243_number_sets.txt", "r") as fh:
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            nums = line.strip().split(",")
            initial_state = list(int(n) for n in nums)
            reachable_targets = countdown_dfs(initial_state)
            reachable_targets = [num for num in reachable_targets if 100 <= num <= 999]
            this_sum = len(reachable_targets)
            total += this_sum
            if idx%100==0:
                print(f"Line {idx} cleared, this line sum is {this_sum}, cumul time is {time.time()-start_time}")
    print(total)
    