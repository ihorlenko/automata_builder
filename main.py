from automata import DFA, NFA, eNFA, State

dfa = DFA()
dfa.start_state = 'q0'
dfa.accept_states = {'q1'}
dfa.update_transition(["q0>a>q1",
                       "q0>b>q3",
                       "q1>b>q0",
                       "q1>a>q2",
                       "q2>a>q3",
                       "q2>b>q3",
                       "q3>a>q3",
                       "q3>b>q3"])

print(dfa)
for elem in dfa.states:
    elem.name = "0"

print(dfa)

