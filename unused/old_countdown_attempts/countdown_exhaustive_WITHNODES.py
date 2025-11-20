# Hayden Schennum
# 2025-11-19

from itertools import combinations
import cProfile

# interp. an operation applied to 2 numbers used to move from one node -> another node
# Oper is one of: ADD, SUB, MUL, DIV
ADD = 1
SUB = 2
MUL = 3
DIV = 4


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



def apply_operation(a,b,oper):
    """
    int int Oper -> int | None
    given 2 chosen numbers and operation; returns the resulting number
    note: input numbers AND result must be positive integers
    """
    if a > b:
        a,b = b,a # so in the following: b >= a
    if oper == ADD:
        return b + a
    elif oper == SUB and a != b:
        return b - a
    elif oper == MUL:
        return b * a
    elif oper == DIV and b % a == 0:
        return b // a
    else:
        return None


def expand(node):
    """
    Node -> next(Node)
    given node, yields the next node in the set of children nodes
    """
    s = node.state
    for i,j in combinations(range(len(s)),2):
        a, b = s[i], s[j]
        for oper in [ADD,SUB,MUL,DIV]:
            result = apply_operation(a, b, oper)
            if result is None:
                continue
            sP = (result,) + s[:i] + s[i+1:j] + s[j+1:] # j > i guaranteed
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
    frontier = [Node(state=initial_state)]  # LIFO queue (stack)
    while frontier != []:
        node = frontier.pop()
        for child in expand(node):
            for num in child.state:
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
    
    cProfile.run('profiler()')
