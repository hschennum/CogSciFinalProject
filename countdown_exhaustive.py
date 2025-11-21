# Hayden Schennum
# 2025-11-19

import time


# Node is tuple<int>|list<int> - current number set

def expand(node):
    """
    Node -> next(Node)
    given node, yields the next node in the set of children nodes
    INVARIANT: all elements of any number set must be positive integers
    """
    idx_range = range(len(node))
    for i in idx_range:
        for j in range(i+1, len(node)):
            a, b = node[i], node[j]
            if a > b:
                a,b = b,a # so b >= a in the following
            
            new_numbers = [b + a]
            if b > a:
                new_numbers.append(b - a)
            new_numbers.append(b * a)
            if b % a == 0:
                new_numbers.append(b // a)
            
            for new_num in new_numbers:
                child = [new_num]
                for k in idx_range:
                    if k != i and k != j:
                        child.append(node[k])
                yield child


def countdown_dfs(initial_state):
    """
    tuple<int> -> set<int>
    given starting number set; returns set of all reachable targets
    """
    reachable = set() # set<int> - target numbers (100-999) that have been reached
    for num in initial_state:
        if 100 <= num <= 999:
            reachable.add(num)
    frontier = [initial_state] # list<tuple<int>> - LIFO queue; UNSORTED number sets that still need to be expanded (newest number is leftmost)
    initial_key = tuple(sorted(initial_state))
    visited = {initial_key} # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    while len(frontier) > 0:
        current_numbers = frontier.pop()
        if len(current_numbers) == 1:
            continue
        for child in expand(current_numbers): # child is a "remaining_numbers" set after applying 1 oper to 2 nums in current_numbers
            for num in child:
                if 100 <= num <= 999:
                    reachable.add(num)
            if len(child) == 1:
                continue
            new_key = tuple(sorted(child))
            if new_key not in visited:
                visited.add(new_key)
                frontier.append(child)
    return reachable


# 1000_number_sets.txt -> should be 1103400 solvable
# 1226_perfect_sets.txt -> should be 1103400 solvable
# 13243_number_sets.txt -> should be 10871986 solvable
if __name__ == "__main__":
    print("Starting")
    start_time = time.time()
    total = 0
    # with open("13243_number_sets.txt", "r") as fh:
    # with open("1226_perfect_sets.txt", "r") as fh:
    with open("1000_number_sets.txt", "r") as fh:
        for idx,line in enumerate(fh,1):
            nums = line.strip().split(",")
            initial_state = tuple(int(n) for n in nums)
            reachable_targets = countdown_dfs(initial_state)
            this_sum = len(reachable_targets)
            total += this_sum
            if (idx)%100==0:
                print(f"Line {idx} cleared, this line sum is {this_sum}, cumul time is {time.time()-start_time}")
    print(f"Finished processing {idx} lines, total time is {time.time()-start_time}")
    print(total)

    
