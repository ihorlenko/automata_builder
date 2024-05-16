## Abstract

This project provides Python implementations of three types of finite automata: Deterministic Finite Automaton (DFA), Non-deterministic Finite Automaton (NFA), and epsilon-NFA. These automata are essential for understanding the theoretical foundations of computer science and are widely used in areas such as lexical analysis, parsing, and regular expression matching. The project includes classes and methods for defining states, transitions, and acceptance conditions, as well as functions for recognizing strings, handling epsilon transitions, and converting between different types of automata.
## Features

-   **DFA (Deterministic Finite Automaton)**:
    
    -   Transition functions
    -   State management
    -   String recognition
-   **NFA (Non-deterministic Finite Automaton)**:
    
    -   Transition functions
    -   Epsilon transitions
    -   String recognition
-   **Epsilon-NFA (NFA with epsilon transitions)**:
    
    -   Epsilon closure computation
    -   Conversion to NFA
    -   Determinization to DFA

## Classes and Methods

### DFA Class

-   **DFA.TransitionFunction**
    
    -   `__getitem__(self, item)`
    -   `__contains__(self, item)`
    -   `__repr__(self)`
    -   `add(self, transition)`
-   **DFA Methods**
    
    -   `__init__(self)`
    -   `__getitem__(self, item)`
    -   `__repr__(self)`
    -   `__len__(self)`
    -   `update_transition(self, transitions_input)`
    -   `add_transition(self, transition)`
    -   `recognize(self, word)`

### NFA Class

-   **NFA.TransitionFunction**
    
    -   `__getitem__(self, item)`
    -   `__contains__(self, item)`
    -   `__repr__(self)`
    -   `add(self, transition)`
-   **NFA Methods**
    
    -   `__init__(self)`
    -   `__getitem__(self, item)`
    -   `__repr__(self)`
    -   `__len__(self)`
    -   `update_transition(self, transitions_input)`
    -   `add_transition(self, transition)`
    -   `recognize(self, word)`
    -   `epsilon_closure(self, states)`
    -   `eliminate_epsilon(self)`
    -   `determinize(self)`

### Epsilon-NFA Class

-   **Epsilon-NFA Methods**
    -   `__init__(self)`
    -   `epsilon_closure(self, states)`
    -   `add_transition(self, transition)`
    -   `recognize(self, word)`
    -   `eliminate_epsilon(self)`
    -   `determinize(self)`

## Getting Started

### Prerequisites

-   Python 3.6 or higher

### Installation

Clone the repository:

`git  clone  https://github.com/your-username/automata-theory-project.git`

### Usage

1.  Import the necessary classes from the `automata.py` file.

`from  automata  import  DFA, NFA, epsilonNFA`

2.  Create instances of the automata and define transitions.

`# DFA example  dfa = DFA() dfa.add_transition('q0>a>q1') dfa.add_transition('q1>b>q2')  # Add more transitions as needed`

3.  Recognize strings.

`result = dfa.recognize('ab')  print(f'The string is  {"accepted"  if  result  else  "rejected"}by the DFA.')`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

-   Thanks to the authors and contributors of various automata theory resources and textbooks (Hopcroft, Ullman).
