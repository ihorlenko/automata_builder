from automata import DFA, NFA, eNFA

dfa1 = DFA()
dfa1._start_state = 'q0'
dfa1._accept_states = {'q1'}
dfa1.update_transition([
    "q0>a>q1",
    "q0>b>q3",
    "q1>b>q0",
    "q1>a>q2",
    "q2>a>q3",
    "q2>b>q3",
    "q3>a>q3",
    "q3>b>q3"
])

dfa2 = DFA()
dfa2._start_state = "q6"
dfa2._accept_states = {"q9"}
dfa2.update_transition([
    "q6>a>q10",
    "q6>b>q9",
    "q7>a>q6",
    "q7>b>q10",
    "q10>a>q10",
    "q10>b>q9",
    "q9>a>q7",
    "q9>b>q9",
])

dfa3 = DFA()
dfa3._start_state = "q0"
dfa3._accept_states = {"q1"}
dfa3.update_transition([
    "q0>a>q1",
    "q0>b>q2",
    "q1>a>q2",
    "q1>b>q0",
    "q2>b>q1",
])

print(dfa3.kleene_star())
print((dfa3.kleene_star()).recognize("aabbbaababa"))
# print(dfa2)

# print(dfa1.union(dfa2))
