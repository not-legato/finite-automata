# NFA / DFA model
The purpose of this project is to provide implementations of finite automata that are isomorphic to their formal counterparts. The implementations are as close to as described in literature for educational purposes. The deterministic model is complete, but the nondeterministic finite automata are too computationally expensive to simulate due to unbound recursion, so we only provide a method to convert from NFA to DFA.

# NFA -> DFA conversion
The function `NFAtoDFA` provides conversion to the deterministic counterpart via the powerset construction present in literature. The design of the code is a little clumsy and will be improved upon later.

This process is described in more detail in Michael Sipser's book "Introduction to the Theory of Computation".

# DFA
Suppose you want to create a DFA whose alphabet is {0, 1} and that accepts all strings containing "001":

![](https://i.imgur.com/9jZah6p.png)

You would construct this automaton in much the same way as it is presented in the theory, though (temporarily) we use tuples over sets:

    Q = ("a", "b", "c", "d")            # possible states
    Sigma = ("0", "1")                  # alphabet
    delta = transition_function({       # transition function
        "a": {"0": "b", "1": "a"}, \
        "b": {"0": "c", "1": "a"}, \
        "c": {"0": "c", "1": "d"}, \
        "d": {"0": "d", "1": "d"}})
    q0 = "a"                            # starting state
    F = ("d",)                          # set of accept states
    M = DFA(Q, Sigma, delta, q0, F)     # finished machine

After that, you can use the DFA to check whether a string is part of its language by using `M.read("1110100111010111011")`, which would return `True`.

# NFA

Here's an example of a simple machine:

    Q = ("1", "2", "3")
    Sigma = ("a", "b")
    delta = transition_function({
        "1": {"b": ("2",), "epsilon": ("3",)}, \
        "2": {"a": ("2", "3"), "b": ("3",)}, \
        "3": {"a": ("1", "3")}})
    q0 = "1"
    F = ("1",)
    N = NFA(Q, Sigma, delta, q0, F)

If you run the machine through the conversion function, ie. `NFAtoDFA(N)`, you'll get the powerset construction of the equivalent DFA. You can test what strings it accepts then as you would with the regular DFAs.

You can also print the machine itself to see its representation more clearly.

# Why not simulate NFA fully?
Suppose you have an NFA with 15 states, and an alphabet with two characters. Suppose also that both inputs lead to all 15 remaining states no matter where you are. Now to check a string with length n, you must do 15<sup>n</sup> operations.

# TODO

* Redesign the code to use sets instead of tuples for both efficiency and consistency of notation with the literature.

* Improve string representation of the machines.

* Later, design a graphical user interface to display the machine as a planar graph.