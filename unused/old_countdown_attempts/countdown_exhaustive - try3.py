# Hayden Schennum
# 2025-11-19

from itertools import combinations
import cProfile

# interp. each operation applied to 2 numbers used to move from one node -> another node
# OPS_DICT is dict<str:(int int -> int|None)>
# only positive integers allowed for input and output (so no need to check for divide by 0)
OPS_DICT = {
    "ADD": lambda x, y: x + y,
    "SUB": lambda x, y: x - y if x > y else (y - x if y > x else None),
    "MUL": lambda x, y: x * y,
    "DIV": lambda x, y: x // y if x % y == 0 else (y // x if y % x == 0 else None)
}


class Node():
    """
    interp. a path and contains state+path_cost info
    Node has:
        state is tuple<int> - the current number set
        parent is Node - pointer to previous node (before oper was applied to nums)
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
    """
    s = node.state
    for i,j in combinations(range(len(s)),2):
        a, b = s[i], s[j]
        for oper in ["ADD","SUB","MUL","DIV"]:
            res = OPS_DICT[oper](b,a)
            if res is None:
                continue
            sP = (res,) + s[:i] + s[i+1:j] + s[j+1:] # j > i guaranteed
            yield Node(state=sP, parent=node, action=(a, b, oper))



def countdown_dfs(initial_state):
    """
    set<int> -> int
    given starting number set; returns qty of reachable targets from 100-999 inclusive
    """
    reachable = set() # only will contain targets in 100-999 inclusive
    for num in initial_state:
        if 100 <= num <= 999:
            reachable.add(num)
    frontier = [Node(state=initial_state)]  # LIFO queue of nodes still needed to be processed
    while frontier != []:
        node = frontier.pop()
        for child in expand(node):
            for num in child.state:
                if 100 <= num <= 999:
                    reachable.add(num)
            frontier.append(child)
    return len(reachable)


def countdown_dfs_cache(initial_state):
    """
    set<int> -> int
    given starting number set; returns qty of reachable targets from 100-999 inclusive
    """
    reachable = set() # only will contain targets in 100-999 inclusive
    for num in initial_state:
        if 100 <= num <= 999:
            reachable.add(num)
    frontier = [Node(state=initial_state)]  # LIFO queue (stack)
    reached = set() # previously-reached states
    while frontier != []:
        node = frontier.pop()
        if frozenset(node.state) in reached:
            continue
        reached.add(frozenset(node.state))
        for child in expand(node):
            for num in child.state:
                if 100 <= num <= 999:
                    reachable.add(num)
            frontier.append(child)
    return len(reachable)




def profiler():
    numbers = (1,3,7,10,25,50)
    # print(countdown_dfs(numbers))
    print(countdown_dfs_cache(numbers))


if __name__ == "__main__":
    # cProfile.run('profiler()')
    total = 0
    # with open("13243_number_sets.txt", "r") as fh:
    with open("1226_perfect_sets.txt", "r") as fh:
        for idx,line in enumerate(fh):
            clean_line = line.strip().replace("{", "").replace("}", "")
            nums = clean_line.strip().split(",")
            initial_state = tuple(int(n) for n in nums)
            this_sum = countdown_dfs_cache(initial_state)
            total += this_sum
            # if idx%100==0:
            print(f"Line {idx} cleared, this line sum is {this_sum}")
    print(total)
    
    
