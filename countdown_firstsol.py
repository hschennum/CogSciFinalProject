# Hayden Schennum
# 2025-11-20

from collections import defaultdict
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


def reconstruct_expression(node, target):
    """
    Node int -> str
    given winning node and target; returns the math expression corresponding to node 
    """
    path = [] # leaf -> root
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()   # now root -> leaf

    if target == 606:
        x=1

    num2expr = defaultdict(list) # dict<int:list<str>> - each number and all current expressions to reach it (can have 2 of same # at once)
    for n in path[0].state:
        num2expr[n].append(str(n))

    for i in range(1, len(path)):
        node = path[i]
        a, b, oper = node.action
        expr_a = num2expr[a].pop()
        expr_b = num2expr[b].pop()
        new_expr = f"({expr_b}{oper}{expr_a})"

        result = None # the number result of (b oper a)
        if oper == '+':
            result = b + a
        elif oper == '-':
            result = b - a
        elif oper == '*':
            result = b * a
        elif oper == '/':
            result = b // a
        
        num2expr[result].append(new_expr)
        if not num2expr[a]:
            del num2expr[a]
        if not num2expr[b]:
            del num2expr[b]
    
    expr = num2expr[target][0]
    if expr.startswith("(") and expr.endswith(")"):
        expr = expr[1:-1]
    return expr


def countdown_dfs(initial_state, target):
    """
    tuple<int> int -> str|None
    given starting number set and target; returns solution expression (or None if unsolvable)
    """
    if target in initial_state:
        return str(target)
    frontier = [Node(initial_state)] # list<Node> - LIFO queue; UNSORTED number sets that still need to be expanded (newest number is leftmost)
    visited = set() # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    initial_key = tuple(sorted(initial_state))
    visited.add(initial_key)
    while len(frontier) > 0:
        current_node = frontier.pop()
        if len(current_node.state) == 1:
            continue
        for child in expand(current_node): # child is a "remaining_numbers" set after applying 1 oper to 2 nums in current_numbers
            s = child.state
            if target in s:
                return reconstruct_expression(child,target)
            if len(s) == 1:
                continue
            new_key = tuple(sorted(s))
            if new_key not in visited:
                visited.add(new_key)
                frontier.append(child)
    return None


# 1226_perfect_sets.txt -> should be 1103400 solvable
# 13243_number_sets.txt -> should be 10871986 solvable
if __name__ == "__main__":
    print("Starting")
    start_time = time.time()

    with open("scraped_full.txt", "r") as fh:
        for idx,line in enumerate(fh,1):
            fields = line.strip().split(";")
            if len(fields) != 7:
                print(f"MALFORMED LINE AT IDX {idx}")
                break
            nums = tuple(int(n) for n in fields[3].split(","))
            target = int(fields[4])

            solution = countdown_dfs(nums, target)
            
            if (idx)%100==0:
                print(f"Line {idx}, Target: {target}, Expression: {solution}, cumul time is {time.time()-start_time}")
    print(f"Finished processing {idx} lines, total time is {time.time()-start_time}")


