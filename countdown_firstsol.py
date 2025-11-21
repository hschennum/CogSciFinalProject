# Hayden Schennum
# 2025-11-20

import time


class Node():
    """
    interp. current state and the path (of prev node + action) to reach it
    Node has:
        state is list<int> - the current number set
        parent is Node - previous node (before oper was applied to nums)
        action is (int,int,Oper) - 2 chosen numbers and chosen operation used to move from parent to this node
    """
    def __init__(self,state,parent=None,action=None):
        self.state = state
        self.parent = parent
        self.action = action


def expand(node):
    """
    Node -> next(Node)
    given node, yields the next node in the set of children nodes
    INVARIANT: all elements of any number set must be positive integers
    """
    s = node.state
    idx_range = range(len(s))
    for i in idx_range:
        for j in range(i+1, len(s)):
            a, b = s[i], s[j]
            if a > b:
                a,b = b,a # so b >= a in the following
            
            new_numbers = [(b + a, '+')]
            if b > a:
                new_numbers.append((b - a, '-'))
            new_numbers.append((b * a, '*'))
            if b % a == 0:
                new_numbers.append((b // a, '/'))
            
            for new_num,oper in new_numbers:
                child_state = [new_num]
                for k in idx_range:
                    if k != i and k != j:
                        child_state.append(s[k])
                yield Node(child_state, parent=node, action=(a, b, oper))


def reconstruct_expression(node):
    """
    Node int -> str
    given winning node, returns the math expression corresponding to node 
    """
    ...


def countdown_dfs(initial_state, target):
    """
    set<int> int -> str|None
    given starting number set and target; returns solution expression (or None if unsolvable)
    """
    if target in initial_state:
        return reconstruct_expression(Node(initial_state))
    frontier = [Node(initial_state)] # list<Node> - LIFO queue; UNSORTED number sets that still need to be expanded (newest number is leftmost)
    visited = set() # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    initial_key = tuple(sorted(initial_state))
    visited.add(initial_key)
    while len(frontier) > 0:
        current_node = frontier.pop()
        if len(current_node.state) == 1:
            continue
        for child in expand(current_node): # child is a "remaining_numbers" set after applying 1 oper to 2 nums in current_numbers
            if target in child.state:
                return reconstruct_expression(child)
            new_key = tuple(sorted(child))
            if new_key not in visited:
                visited.add(new_key)
                frontier.append(child)
    return reachable


# 1226_perfect_sets.txt -> should be 1103400 solvable
# 13243_number_sets.txt -> should be 10871986 solvable
if __name__ == "__main__":
    print("Starting")
    start_time = time.time()
    total = 0
    # with open("13243_number_sets.txt", "r") as fh:
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            nums = line.strip().split(",")
            initial_state = tuple(int(n) for n in nums)
            reachable_targets = countdown_dfs(initial_state)
            this_sum = len(reachable_targets)
            total += this_sum
            if (idx+1)%100==0:
                print(f"Line {idx+1} cleared, this line sum is {this_sum}, cumul time is {time.time()-start_time}")
    print(f"Finished processing {idx+1} lines, total time is {time.time()-start_time}")
    print(total)

    
