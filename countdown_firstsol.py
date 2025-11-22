# Hayden Schennum
# 2025-11-20

from collections import defaultdict
import heapq
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



def countdown_depth_limited(initial_state, target, max_depth):
    """
    tuple<int> int int -> str|None
    given starting number set, target, and max depth to search; returns solution expression (or None if unsolvable)
    """
    if target in initial_state:
        return str(target)
    frontier = [(Node(initial_state), 0)]  # list<(Node, int)> - nodes that still need to be expanded AND corresponding depths
    initial_key = tuple(sorted(initial_state))
    visited = {initial_key} # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    while len(frontier) > 0:
        current_node, depth = frontier.pop()
        if len(current_node.state) == 1 or depth >= max_depth:
            continue
        for child in expand(current_node):
            s = child.state
            if target in s:
                return reconstruct_expression(child, target)
            if len(s) == 1:
                continue
            new_key = tuple(sorted(s))
            if new_key not in visited:
                visited.add(new_key)
                frontier.append((child, depth+1))
    return None


def countdown_iterdeep(initial_state, target):
    """
    tuple<int> -> set<int>
    given starting number set and target; returns solution expression (or None if unsolvable)
    """
    for max_depth in range(1, 6): # final max_depth used should be 5 (depth 5 corresponds to using 6 numbers)
        solution = countdown_depth_limited(initial_state, target, max_depth)
        if solution is not None:
            return solution
    return None




def countdown_dfs(initial_state, target):
    """
    tuple<int> int -> str|None
    given starting number set and target; returns solution expression (or None if unsolvable)
    """
    if target in initial_state:
        return str(target)
    frontier = [Node(initial_state)] # list<Node> - LIFO queue; UNSORTED number sets that still need to be expanded (newest number is leftmost)
    initial_key = tuple(sorted(initial_state))
    visited = {initial_key} # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    while len(frontier) > 0:
        current_node = frontier.pop()
        if len(current_node.state) == 1:
            continue
        for child in expand(current_node): # child is a "remaining_numbers" set after applying 1 oper to 2 nums in current_numbers
            s = child.state
            if target in s:
                return reconstruct_expression(child, target)
            if len(s) == 1:
                continue
            new_key = tuple(sorted(s))
            if new_key not in visited:
                visited.add(new_key)
                frontier.append(child)
    return None



def countdown_bfs_prox(initial_state, target):
    """
    tuple<int> int -> str|None
    given starting number set and target; returns solution expression (or None if unsolvable)
    """
    if target in initial_state:
        return str(target)
    frontier = [] # list<(int, int, tuple<int>)> - priority queue (min-heap); heuristic measure AND tie-breaking counter AND number sets that still need to be expanded
    initial_h = min(abs(num - target) for num in initial_state)
    counter = 0 # breaks ties if 2 nodes have same heuristic measure
    heapq.heappush(frontier, (initial_h, counter, Node(initial_state)))
    initial_key = tuple(sorted(initial_state))
    visited = {initial_key} # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    while len(frontier) > 0:
        _, _, current_node = heapq.heappop(frontier)
        if len(current_node.state) == 1:
            continue
        for child in expand(current_node):
            s = child.state
            if target in s:
                return reconstruct_expression(child, target)
            if len(s) == 1:
                continue
            new_key = tuple(sorted(s))
            if new_key not in visited:
                visited.add(new_key)
                h = min(abs(num - target) for num in s)
                counter += 1
                heapq.heappush(frontier, (h, counter, child))
    return None



def countdown_bfs_prox_factor(initial_state, target, alpha, beta):
    """
    tuple<int> int float int -> str|None
    given starting number set, target, factor bonus, and factor threshold; returns solution expression (or None if unsolvable)
    """
    def heuristic(nums):
        """
        tuple<int> -> float
        given number set; returns corresponding proximity+factor heuristic measure
        """
        min_so_far = float('inf')
        for s in nums:
            base = abs(s - target)
            bonus = base - alpha*target if target % s == 0 and s >= beta else base
            if bonus < min_so_far:
                min_so_far = bonus
        return min_so_far
    if target in initial_state:
        return str(target)
    frontier = [] # list<(int, int, tuple<int>)> - priority queue (min-heap); heuristic measure AND tie-breaking counter AND number sets that still need to be expanded
    initial_h = heuristic(initial_state)
    counter = 0
    heapq.heappush(frontier, (initial_h, counter, Node(initial_state)))
    initial_key = tuple(sorted(initial_state))
    visited = {initial_key} # set<tuple<int>> - SORTED number sets that have already been seen (don't need to re-expand)
    while len(frontier) > 0:
        _, _, current_node = heapq.heappop(frontier)
        if len(current_node.state) == 1:
            continue
        for child in expand(current_node):
            s = child.state
            if target in s:
                return reconstruct_expression(child, target)
            if len(s) == 1:
                continue
            new_key = tuple(sorted(s))
            if new_key not in visited:
                visited.add(new_key)
                h = heuristic(s)
                counter += 1
                heapq.heappush(frontier, (h, counter, child))
    return None



def evaluate_params(alpha, beta, filepath):
    """
    float int str -> int float
    given factor bonus, factor threshold, and input file;
    returns amount of problems solved and total time taken
    """
    start_time = time.time()
    solved = 0
    with open(filepath, "r") as fh:
        for line in fh:
            fields = line.strip().split(";")
            if len(fields) != 7:
                continue
            nums = tuple(int(n) for n in fields[3].split(","))
            target = int(fields[4])
            if countdown_bfs_prox_factor(nums, target, alpha, beta) is not None:
                solved += 1
    total_time = time.time() - start_time
    return solved, total_time


if __name__ == "__main__":
    start_time = time.time()
    solved = 0
    unsolved = 0
    with open("scraped_full.txt", "r") as fh:
    # with open("scraped_10000.txt", "r") as fh:
    # with open("T_only_scraped_10000.txt", "r") as fh:
    # with open("F_only_scraped_10000.txt", "r") as fh:
    # with open("scraped_1000_gridsearch.txt", "r") as fh:
        for idx,line in enumerate(fh,1):
            fields = line.strip().split(";")
            if len(fields) != 7:
                print(f"MALFORMED LINE AT IDX {idx}")
                break
            num_field = [int(n) for n in fields[3].split(",")]
            nums = tuple(num_field)
            target = int(fields[4])
            # solution = countdown_dfs(nums, target)
            # solution = countdown_iterdeep(nums, target)
            # solution = countdown_bfs_prox(nums, target)
            solution = countdown_bfs_prox_factor(nums, target, .9, 1)
            if solution is None:
                unsolved += 1
                print(f"Unsolved line at idx {idx}")
            else:
                solved += 1
            if idx%1000==0:
                print(f"Line {idx}, Target: {target}, Expression: {solution}, cumul time is {time.time()-start_time}")
    print(f"Finished processing {idx} lines, total time is {time.time()-start_time}")
    print(f"Solved: {solved}, Unsolved: {unsolved}")


    # # alpha_range = [i*0.1 for i in range(0, 11)]
    # # alpha_range = [i*0.1 for i in range(11, 16)]
    # # alpha_range = [i*0.1 for i in range(16, 21)]
    # # beta_range = list(range(1, 21))
    # alpha_range = [i*0.1 for i in range(8, 11)]
    # beta_range = list(range(1, 4))
    # best_time = float('inf')
    # best_params = None
    # with open("param_results.txt", "w", buffering=1) as out_file:
    #     out_file.write("alpha\tbeta\tsolved\ttime\n")
    #     for alpha in alpha_range:
    #         for beta in beta_range:
    #             solved, total_time = evaluate_params(alpha, beta, "scraped_10000.txt")
    #             # solved, total_time = evaluate_params(alpha, beta, "scraped_1000_gridsearch.txt")
    #             out_file.write(f"{alpha}\t{beta}\t{solved}\t{total_time:.4f}\n")
    #             print(f"alpha={alpha}, beta={beta}, solved={solved}, time={total_time:.4f}s")
    #             if solved == 10000 and total_time < best_time:
    #                 best_time = total_time
    #                 best_params = (alpha, beta)
    # print("Best params:", best_params, "Time:", best_time)



# nums = tuple(sorted(num_field,reverse=True))

# for DFS without memoization (not like you'd ever want to), swap
    # new_key = tuple(sorted(s))
    # if new_key not in visited:
    #     visited.add(new_key)
    #     frontier.append(child)
# with
    # frontier.append(child)
            