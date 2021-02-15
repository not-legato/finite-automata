from itertools import chain, combinations # for powersets

# This model of a DFA is completely equivalent to the formal definition.
class DFA:
    def __init__(self, Q: set, Sigma: set, delta, q0, F: set):
        self.states = Q
        self.alphabet = Sigma
        self.delta = delta
        self.start = q0
        self.accept = F
        self.position = q0

    # checks whether the machine recognises the string.
    def read(self, s: str):
        if not set(s).issubset(self.alphabet):
            return False
        for c in s:
            self.position = self.delta(self.position, c)
        if self.position in self.accept:
            self.resetPosition()
            return True
        else:
            self.resetPosition()
            return False

    def resetPosition(self):
        self.position = self.start

    def __str__(self):
        representations = []
        rep = ""
        for state in self.states:
            rep += f"{state}: " + "{"
            for c in self.alphabet:
                rep += f"{c} -> {self.delta(state, c)}, "
            rep = rep[:-2] + "}"
            representations.append(rep)
            rep = ""
        return "\n".join(sorted(representations))
    
# for now, this NFA model only serves to be converted to DFA.
# delta must be a function tuple -> tuple: delta((states), input) = (more states)
class NFA:
    def __init__(self, Q: dict, Sigma: set, delta, q0: str, F: set):
        self.states = Q
        self.alphabet = Sigma
        self.delta = delta # this shows what arrows are connected to what state.
        self.start = q0
        self.accept = F

    def __str__(self):
        representations = []
        rep = ""
        for state in self.states:
            rep += f"{state}: " + "{"
            for c in self.alphabet + ("epsilon",):
                try:
                    temp = "{" + ", ".join(self.delta(state, c)) + "}"
                    rep += f"{c} -> {temp}, "
                except:
                    continue
            rep = rep[:-2] + "}"
            representations.append(rep)
            rep = ""
        return "\n".join(sorted(representations))

def powerset(data: set):
    Pdata = tuple([*chain.from_iterable(combinations(data, r) for r in range(len(data) + 1))])
    return Pdata

# powerset construction.
def NFAtoDFA(M: NFA):
    Q_prime = powerset(M.states)
    F_prime = set([R for R in Q_prime if set(R).intersection(M.accept)]) # all subsets of P(Q) containing an accept state.

    # R is an element of Q' = P(Q).
    # deltaprime = d'(R,a) = {q in Q : q in d(r,a) for r in R}, where
    # d refers to M.arrows() and Q to M.states.
    def deltaprime(R: tuple, input: str):
        union = ()
        for state in R:
            try:
                union += M.delta(state, input)
            except:
                continue
        return union

    # E(R) as defined in Michael Sipser's "Introduction to the Theory of Computation".
    # takes a set (tuple) of states and appends all states connected by outgoing
    # epsilon-arrows.
    def E(states: tuple):
        epsilon_paths = ()
        for state in states:
            if deltaprime(state, "epsilon"): # not empty
                epsilon_paths += (deltaprime(state, "epsilon"))
        return states + epsilon_paths

    # redefine d' to include epsilon-paths.
    def delta_prime(states: tuple, input: str):
        return tuple(sorted(list(set(E(deltaprime(states, input)))))) # oh no. using sets will fix this.

    q0 = E(tuple(M.start)) # start state must contain empty string connections.

    # the theoretical construction is now complete.
    return DFA(Q_prime, M.alphabet, delta_prime, q0, F_prime)

# if a state has no arrows pointing to it (and is not a start state),
# remove from machine.
def minimise(M: DFA):
    found_nodes = {M.start}
    for state in M.states:
        for c in M.alphabet:
            connection = M.delta(state, c)
            if state != connection:
                found_nodes.add(connection)
    M.states = tuple(found_nodes)

def transition_function(instructions: dict):
    def delta(state, input):
        return instructions[state][input]
    return delta

if __name__ == "__main__":

    # # this is Example 1.16 from Sipser.
    print("A few tests:")
    Q = ("1", "2", "3")
    Sigma = ("a", "b")
    delta = transition_function({
        "1": {"b": ("2",), "epsilon": ("3",)}, \
        "2": {"a": ("2", "3"), "b": ("3",)}, \
        "3": {"a": ("1", "3")}})
    q0 = "1"
    F = ("1",)
    N = NFA(Q, Sigma, delta, q0, F)
    # convert the machine to DFA via the powerset construction.
    M = NFAtoDFA(N)
    # tests as per Sipser
    trues = ["", "a", "baba", "baa"]
    falses = ["b", "bb", "babba"]
    print("These should be true.")
    for i in trues:
        print(M.read(i))
    print("These should be false.")
    for j in falses:
        print(M.read(j))
    print("This is the original NFA.")
    print(N)
    print("This is the converted DFA.")
    print(M)
    minimise(M)
    print("Now with the inaccessible nodes cut.")
    print(M)