from automata import DFA, NFA

nfa = NFA()
nfa._start_state = 'q0'
nfa._accept_states = {'q3'}
nfa.update_transition(["q0>0>q1", "q0>1>q2", "q1>1>q3", "q2>0>q3", "q0>0>q3"])
dfa = nfa.determinize()
# dfa = DFA()
# dfa._start_state = 'q0'
# dfa._accept_states = {'q3', "q0"}
# dfa.update_transition(["q0>0>q1", "q0>1>q2", "q1>1>q3", "q2>0>q3"])

print(dfa)
