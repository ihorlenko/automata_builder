class DFA(NFA):
    class TransitionFunction:
        def __init__(self):
            self.__data = {}

        def __getitem__(self, item):
            return self.__data[item]

        def __contains__(self, item):
            return item in self.__data

        def __repr__(self):
            representation = ""
            for state in self.__data:
                representation += f"{str(state)}: {str(self.__data[state])}\n"
            return f"{representation}"

        def add(self, transition):
            state, symbol, next_state = transition.split('>')
            if state not in self.__data:
                self.__data[state] = {}
            self.__data[state][symbol] = next_state

    def __init__(self):
        self.states = set()
        self._start_state = None
        self.alphabet = set()
        self.transition_function = self.TransitionFunction()
        self._accept_states = None

    def __getitem__(self, item: str) -> dict[str, str]:
        return self.transition_function[item]

    def __repr__(self):
        return f"States: {self.states}\n" \
               f"Start state: {self._start_state}\n" \
               f"Alphabet: {self.alphabet}\n" \
               f"Accept states: {self._accept_states}\n" \
               f"Transition function: \n{self.transition_function}"

    def update_transition(self, transitions_input: list[str]):
        for transition in transitions_input:
            self.add_transition(transition)

    def add_transition(self, transition: str):
        state, symbol, next_state = transition.split('>')
        self.states.add(state)
        self.states.add(next_state)
        self.alphabet.add(symbol)
        self.transition_function.add(transition)

    def recognize(self, word):
        current_state = self.start_state
        for symbol in word:
            if symbol not in self.alphabet \
                    or current_state not in self.transition_function \
                    or symbol not in self.transition_function[current_state]:
                return False
            current_state = self.transition_function[current_state][symbol]
        return current_state in self.accept_states

    @property
    def start_state(self):
        return self._start_state

    @property
    def accept_states(self):
        return self._accept_states

    @start_state.setter
    def start_state(self, value):
        if value is not None:
            self.states.add(value)
        self._start_state = value

    @accept_states.setter
    def accept_states(self, value):
        if value is not None:
            self.states.update(value)
        self._accept_states = value


class NFA:
    class TransitionFunction:
        def __init__(self):
            self.__data = {}

        def __getitem__(self, item):
            if item in self.__data:
                return self.__data[item]
            else:
                return set()

        def __contains__(self, item):
            return item in self.__data

        def add(self, transition):
            state, symbol, next_state = transition.split('>')
            if state not in self.__data:
                self.__data[state] = {}
            if symbol not in self.__data[state]:
                self.__data[state][symbol] = set()
            self.__data[state][symbol].add(next_state)

    def __init__(self):
        self.states = set()
        self._start_state = None
        self.alphabet = {"e"}
        self.transition_function = self.TransitionFunction()
        self._accept_states = None

    def __getitem__(self, item: str) -> dict[str, set]:
        return self.transition_function[item]

    def update_transition(self, transitions_input: list[str]):
        for transition in transitions_input:
            self.add_transition(transition)

    def add_transition(self, transition: str):
        state, symbol, next_state = transition.split('>')
        self.states.add(state)
        self.states.add(next_state)
        self.alphabet.add(symbol)
        self.transition_function.add(transition)

    def determinize(self):
        dfa = DFA()
        dfa.alphabet = self.alphabet - {"e"}

        initial_state = frozenset([self._start_state])
        dfa.start_state = ",".join(list(initial_state))
        dfa.states.add(",".join(list(initial_state)))

        unprocessed_states = {initial_state}

        while unprocessed_states:
            current_state = unprocessed_states.pop()

            for symbol in self.alphabet:
                next_states_raw = set()
                for substate in current_state:
                    if symbol in self.transition_function[substate]:
                        next_states_raw.update(self.transition_function[substate][symbol])

                if not next_states_raw:
                    continue

                next_state = ",".join(list(next_states_raw))
                if next_state not in dfa.states:
                    dfa.states.add(next_state)
                    unprocessed_states.add(frozenset(next_states_raw))

                transition = f"{','.join(list(current_state))}>{symbol}>{next_state}"
                dfa.add_transition(transition)

        dfa.accept_states = set()
        for state in dfa.states:
            if any(substate in self._accept_states for substate in state.split(',')):
                dfa.accept_states.add(state)

        return dfa

    def recognize(self, word):
        current_states = {self._start_state}

        for symbol in word:
            next_states = set()
            for state in current_states:
                if symbol in self.transition_function[state]:
                    next_states.update(self.transition_function[state][symbol])
            current_states = next_states

            if not current_states:
                return False

        return any(state in self._accept_states for state in current_states)

    @property
    def start_state(self):
        return self._start_state

    @property
    def accept_states(self):
        return self._accept_states

    @start_state.setter
    def start_state(self, value):
        if value is not None:
            self.states.add(value)
        self._start_state = value

    @accept_states.setter
    def accept_states(self, value):
        if value is not None:
            self.states.update(value)
        self._accept_states = value


class eNFA(NFA):
    def __init__(self):
        super().__init__()
        self.epsilon = 'e'

    def add_epsilon_transition(self, state_from, state_to):
        self.add_transition(f"{state_from}>{self.epsilon}>{state_to}")

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for next_state in self.transition_function[state].get(self.epsilon, []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure


