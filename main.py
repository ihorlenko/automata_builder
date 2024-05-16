from automata import DFA, NFA, eNFA

dfa = DFA()
dfa._start_state = "q0"
dfa._accept_states = {"q0"}
dfa.update_transition([
"q0>0>q1", "q0>1>q3",
"q1>0>q0", "q1>1>q2",
"q2>0>q3", "q2>1>q1",
"q3>0>q2", "q3>1>q0",
])

print(dfa.minimize())

