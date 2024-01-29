class AutomatonInputError(Exception):
    pass

class DFA:
    class TransitionFunction:
        def __init__(self):
            self.__data = {}

        def __getitem__(self, item):
            if item in self.__data:
                return self.__data[item]
            else:
                return dict()

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
            if symbol in self.__data[state]:
                raise AutomatonInputError("DFA mustn't contain non-deterministic transitions")
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
        return f"{type(self)}\n" \
               f"States: {self.states}\n" \
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

    def reverse(self):
        enfa = eNFA()
        enfa.alphabet = self.alphabet

        terminal_state = f"q{len(self.states)}"
        enfa.start_state = terminal_state
        enfa.accept_states = {self.start_state}

        for state in self.states:
            for symbol, next_state in self.transition_function[state].items():
                enfa.add_transition(f"{next_state}>{symbol}>{state}")
            if state in self.accept_states:
                enfa.add_epsilon_transition(terminal_state, state)

        return enfa

    def minimize(self):
        r = self.reverse()
        dr = r.determinize()
        rdr = dr.reverse()
        drdr = rdr.determinize()
        return drdr

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


class NFA(DFA):
    class TransitionFunction(DFA.TransitionFunction):
        def add(self, transition):
            state, symbol, next_state = transition.split('>')
            if state not in self.__data:
                self.__data[state] = {}
            if symbol not in self.__data[state]:
                self.__data[state][symbol] = set()
            self.__data[state][symbol].add(next_state)

    def __init__(self):
        super().__init__()
        self.transition_function = self.TransitionFunction()

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


class eNFA(NFA):
    def __init__(self):
        super().__init__()
        self.epsilon = 'eps'

    def add_epsilon_transition(self, state_from, state_to):
        self.add_transition(f"{state_from}>{self.epsilon}>{state_to}")

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            if self.epsilon not in self.transition_function[state]:
                continue
            for next_state in self.transition_function[state][self.epsilon]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def add_transition(self, transition: str):
        state, symbol, next_state = transition.split('>')
        self.states.add(state)
        self.states.add(next_state)
        if symbol != "eps":
            self.alphabet.add(symbol)
        self.transition_function.add(transition)

    def recognize(self, word):
        current_states = self.epsilon_closure({self._start_state})

        for symbol in word:
            next_states = set()
            for state in current_states:
                if symbol in self.transition_function[state]:
                    next_states.update(self.transition_function[state][symbol])
                if self.epsilon in self.transition_function[state]:
                    next_states.update(self.transition_function[state][self.epsilon])
            current_states = self.epsilon_closure(next_states)

            if not current_states:
                return False

        return any(state in self._accept_states for state in current_states)

    def eliminate_epsilon(self):
        nfa = NFA()
        nfa.start_state = self.start_state
        nfa.accept_states = set()
        for state in self.states:
            orbit = self.epsilon_closure({state})
            for satellite in orbit:
                for symbol in self.transition_function[satellite]:
                    if symbol == self.epsilon:
                        continue
                    next_states = self.transition_function[satellite][symbol]
                    for next_state in next_states:
                        nfa.add_transition(f"{state}>{symbol}>{next_state}")
            if orbit & self.accept_states != set():
                nfa.accept_states |= orbit

        return nfa

    def determinize(self):
        nfa = self.eliminate_epsilon()
        dfa = nfa.determinize()
        return dfa
