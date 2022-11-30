from typing import Union

class State:
    """State of Levenshtein Automaton"""
    def __init__(self, reject: bool=False, accept: bool=False, transitions: Union[dict, None]=None) -> None:
        self.reject = reject
        self.accept = accept
        self.transitions = transitions
    
    def next_state(self, char: str) -> 'State':
        return self.transitions[char] if char in self.transitions else self.transitions[None]


class LevenshteinAutomaton:
    """Levenshtein Automaton"""
    def __init__(self, string: str, max_dist: int=1) -> None:
        self.string = string
        self.max_dist = max_dist
        self.initial_state = None
        self.construct_automata()

    def construct_automata(self):
        def initial():
            return (range(self.max_dist + 1), range(self.max_dist + 1))

        def step(indices: list, values: list, char: str) -> None:
            if indices and indices[0] == 0 and values[0] < self.max_dist:
                new_indices = [0]
                new_values = [values[0] + 1]
            else:
                new_indices = []
                new_values = []

            for j,i in enumerate(indices):
                if i == len(self.string): break
                cost = 0 if self.string[i] == char else 1
                val = values[j] + cost
                if new_indices and new_indices[-1] == i:
                    val = min(val, new_values[-1] + 1)
                if j+1 < len(indices) and indices[j+1] == i+1:
                    val = min(val, values[j+1] + 1)
                if val <= self.max_dist:
                    new_indices.append(i+1)
                    new_values.append(val)

            return (new_indices, new_values)

        def is_match(indices: list, values: list) -> bool:
            return bool(indices) and indices[-1] == len(self.string)

        def can_match(indices:list, values: list) ->bool:
            return bool(indices)

        def possible_transitions(indices: list, values: list) -> set:
            return [self.string[i] for i in indices if i < len(self.string)] + [None]
    
        def explore(state) -> int:
            key = (tuple(state[0]), tuple(state[1]))
            if key in states:
                return states[key]
            i = len(states)
            states[key] = i
            transitions.append([])
            if is_match(*state):
                accepting.append(i)
            if not can_match(*state):
                rejecting.append(i)
            for char in possible_transitions(*state):
                newstate = step(*state, char)
                j = explore(newstate)
                transitions[i].append((char, j))
            return i

        states = dict()
        accepting = []
        rejecting = []
        transitions = []

        start = initial()
        explore(start)
        automata_states = [State() for _ in range(len(states))]
        self.initial_state = automata_states[states[(tuple(start[0]), tuple(start[1]))]]

        for state in accepting:
            automata_states[state].accept = True
        for state in rejecting:
            automata_states[state].reject = True
        for state in states.values():
            automata_states[state].transitions = {
                char: automata_states[state_key] for char, state_key in transitions[state]
            }

    def accepts(self, word: str) -> bool:
        """Checks if the automaton accepts the word"""
        # Trivial Cases
        if abs(len(word) - len(self.string)) > self.max_dist:
            return False
        if len(word) + len(self.string) <= self.max_dist:
            return True

        self.cur_state = self.initial_state
        for char in word:
            self.cur_state = self.cur_state.next_state(char)
            if self.cur_state.reject:
                return False
        return self.cur_state.accept


def filter_by_levenshtein(string: str, words: 'list[str]', max_dist: int=1) -> 'list[str]':
    automaton = LevenshteinAutomaton(string, max_dist)
    return list(filter(automaton.accepts, words))
