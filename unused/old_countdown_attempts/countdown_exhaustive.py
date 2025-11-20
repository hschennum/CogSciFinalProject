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

# Node is State (only has state, no parent/action info - can't reconstruct path)
# State is tuple<int> - the current number set 

def expand(node):
    """
    Node -> next(Node)
    given node, yields the next node in the set of children nodes
    """
    s = node
    set_range = range(len(s))
    for i,j in combinations(set_range,2):
        a, b = s[i], s[j]
        for oper in ["ADD","SUB","MUL","DIV"]:
            res = OPS_DICT[oper](b,a)
            if res is None:
                continue
            sP = [res] + [s[k] for k in set_range if k != i and k != j]
            yield sP



def countdown_dfs(initial_state):
    """
    tuble<int> -> int
    given starting number set; returns qty of reachable targets from 100-999 inclusive
    """
    reachable = set() # only will contain targets in 100-999 inclusive
    for num in initial_state:
        if 100 <= num <= 999:
            reachable.add(num)
    frontier = [initial_state]  # LIFO queue (stack)
    while frontier != []:
        node = frontier.pop()
        for child in expand(node):
            for num in child:
                if 100 <= num <= 999:
                    reachable.add(num)
            frontier.append(child)
    return len(reachable)







def profiler():
    numbers = (1,3,7,10,25,50)
    print(countdown_dfs(numbers))

if __name__ == "__main__":
    # total = 0
    # with open("13243_number_sets.txt", "r") as fh:
    #     for line in fh:
    #         nums = line.strip().split(",")
    #         initial_state = tuple(int(n) for n in nums)            
    #         total += countdown_dfs(initial_state)
    # print(total)
    
    cProfile.run("profiler()")
