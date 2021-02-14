from itertools import chain, combinations # for powersets

# This model of a DFA is completely equivalent to the formal definition.
class DFA:
    def __init__(self, Q: set, Sigma: set, delta, q0: str, F: set):
        self.states = Q
        self.alphabet = Sigma
        self.transition = delta
        self.start = q0
        self.accept = F
        self.position = q0

    # checks whether the machine recognises the string.
    def read(self, s: str):
        if not set(s).issubset(self.alphabet):
            return False
        for c in s:
            self.position = self.transition(self.position, c)
        if self.position in self.accept:
            self.resetPosition()
            return True
        else:
            self.resetPosition()
            return False

    def resetPosition(self):
        self.position = self.start
    
# for now, this NFA model only serves to be converted to DFA.
# delta must be a function tuple -> tuple: delta((states), input) = (more states)
class NFA:
    def __init__(self, Q: dict, Sigma: set, delta, q0: str, F: set):
        self.states = Q
        self.alphabet = Sigma
        self.delta = delta
        self.start = q0
        self.accept = F

def powerset(data: set):
    return chain.from_iterable(combinations(data, r) for r in range(len(data) + 1))

# this is via the powerset construction.
def NFAtoDFA(M: NFA):
    Q = powerset(M.states)
    F = (R for R in Q if set(R).intersection(M.accept)) # if R contains an accept state, add.

    # E(R) as defined in Michael Sipser's "Introduction to the Theory of Computation".
    # takes a set of states and adds all the epsilon-connected states.
    def E(states: tuple):
        epsilon_paths = tuple()
        for state in states:
            if deltaprime(state, "epsilon"): # not empty
                epsilon_paths += (deltaprime(state, "epsilon"))
        return tuple(states + epsilon_paths)

    # define deltaprime d' as: for R in Q', d'(R,a) = {q in Q : q in d(r,a) for r in R}.
    # Here Q = M.states and Q' = powerset(M.states).
    def deltaprime(states: tuple, input: str):
        union = tuple()
        for state in states:
            union += (M.delta(state, input))
        return tuple(union)

    # redefine delta to include epsilon-paths.
    def delta(states: tuple, input: str):
        return E(deltaprime(states, input))

    q0 = E(tuple(M.start)) # start state must contain empty string connections.

    # the theoretical construction is now complete.
    return DFA(Q, M.alphabet, delta, q0, F)


# if a state has no arrows pointing to it (and is not a start state),
# remove from machine.
def stripDeadEnds(M: DFA):
    pass

# produces a proper transition function out of the dictionary of connections.
def transition_function(instructions: dict):
    def delta(state: str, input: str):
        return instructions[state][input]
    return delta

if __name__ == "__main__":

    Q = {"a", "b", "c", "d"}            # possible states
    Sigma = {"0", "1"}                  # alphabet
    delta = transition_function({       # transition function
        "a": {"0": "b", "1": "a"}, \
        "b": {"0": "c", "1": "a"}, \
        "c": {"0": "c", "1": "d"}, \
        "d": {"0": "d", "1": "d"}})
    q0 = "a"                            # starting state
    F = {"d"}                           # set of accept states
    M = DFA(Q, Sigma, delta, q0, F)     # finished machine
    print(M.read("1110100111010111011"))

    # this is for testing purposes, once the NFAtoDFA function works as intended.
    # # this is Example 1.21 from Sipser.
    # Q = {"1", "2", "3"}
    # Sigma = {"a", "b"}
    # delta = transition_function({"1": {"b": ("2",), "epsilon": ("3",)}, \
    #                             "2": {"a": ("2", "3"), "b": ("3",)}, \
    #                             "3": {"a": ("1", "3")}})
    # q0 = "1"
    # F = {"1"}
    # N = NFA(Q, Sigma, delta, q0, F)
    # M = NFAtoDFA(N)
    # M.read("babba")
    # M.read("baba")