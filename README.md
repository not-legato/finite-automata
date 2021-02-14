# NFA / DFA model
The purpose of this project is to provide implementations of finite automata that are isomorphic to their formal counterparts. The implementations are as close to as described in literature for educational purposes. The deterministic model is complete, but the nondeterministic finite automata are too computationally expensive to simulate due to unbound recursion, so we only provide a method to convert from NFA to DFA. Also in progress. I will update the repository again once

* The conversion yields a functional DFA,

* I have written clearer representations of existing machines.

# NFA -> DFA conversion
This is TODO. It's well-underway, but the construction is tricky to implement in practice.

# DFA
Suppose you want to create a DFA whose alphabet is {0, 1} and that accepts all strings containing "001":

![](https://i.imgur.com/9jZah6p.png)

You would construct this automaton in much the same way as it is presented in the theory:

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

After that, you can use the DFA to check whether a string is part of its language by using `M.read("1110100111010111011")`, which would return `True`.

# NFA
TODO.

# Why not simulate NFA fully?
Suppose you have an NFA with 15 states, and an alphabet with two characters. Suppose also that both inputs lead to all 15 remaining states no matter where you are. Now to check a string with length n, you must do 15<sup>n</sup> operations.