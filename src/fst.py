from typing import Union
from copy import deepcopy


class State:
    def __init__(self):
        self.final: Union[bool, None] = None
        self.transition = {}
        self.output_set: Union[set, None] = None  # for final states only
        self.transition_output = {}

    def clear(self):
        self.final = False
        self.transition.clear()
        # TODO do we need to clear output_set or transition_output as well? Not clear in paper...
        # self.output_set = None
        # self.transition_output.clear()


def create_fst(fp):
    mtsd = {}  # MinimumTransducerStatesDictionary
    MAX_WORDS_SZ = 23  # "electroencephalograph's"

    def find_minimized(s: State):
        """returns an equivalent state from the dict.
         If not present inserts a copy of the parameter to the dictionary and returns it
        """
        hashed = ...  # TODO Hash s
        if hashed not in mtsd:
            r = deepcopy(s)
            mtsd[hashed] = r
            return r
        return mtsd[hashed]

    temp_states = [State()] * MAX_WORDS_SZ  # XXX FST is a DAG, and this variable holds the current "branch"
    prev_word = ''
    temp_states[0].clear()
    with open(fp, 'r') as f:
        for curr_out, curr_word in enumerate(f):  # we are considering the OUTPUT as the WORD POSITION in the input file
            # compute longest common prefix of current and previous words:
            prefixlenp1 = 1
            while prefixlenp1 < len(curr_word) and prefixlenp1 < len(prev_word) and\
                    prev_word[prefixlenp1] == curr_word[prefixlenp1]:
                prefixlenp1 += 1
            # minimize the stats from the suffix of previous word
            # (in terms of https://blog.burntsushi.net/transducers, this means combining existing frozen states to the
            # previous word suffix, which we will know we can now freeze)
            for i in range(len(prev_word), prefixlenp1 - 1, -1):
                temp_states[i-1].transition[prev_word[i]] = find_minimized(temp_states[i])
            # init tail states for current word
            for i in range(prefixlenp1, len(curr_word) + 1):
                temp_states[i].clear()
                temp_states[i-1].transition[curr_word[i]] = temp_states[i]
            if curr_word != prev_word:
                temp_states[len(curr_word)].final = True
                temp_states[len(curr_word)].output_set = {''}
            for j in range(1, prefixlenp1):
                out = temp_states[j-1].transition_output[curr_word[j]]
                common_prefix = min(out, curr_out)  # XXX REMARK in our application, transition outputs are simply ints
                # so their "prefix" is the min function (as mentioned in https://blog.burntsushi.net/transducers)
                word_suffix = out - common_prefix
                temp_states[j-1].transition_output[curr_word[j]] = common_prefix
                for ci in range(256):
                    c = chr(ci)  # convert to char
                    if c in temp_states[j].transition:
                        new_out = word_suffix + temp_states[j].transition_output[c]
                        temp_states[j].transition_output[c] = new_out
                if temp_states[j].final:
                    temp_states[j].output_set = set([word_suffix + t for t in temp_states[j].output_set])
                curr_out -= common_prefix
            if curr_word == prev_word:
                if temp_states[len(curr_word)].output_set is None:
                    temp_states[len(curr_word)].output_set = {curr_out}
                else:
                    temp_states[len(curr_word)].output_set.add(curr_out)
            else:
                temp_states[prefixlenp1-1].transition_output[curr_word[prefixlenp1]] = curr_out
            prev_word = curr_word
        # minimize the states of the LAST word
        for i in range(len(curr_word), 0, -1):
            temp_states[i-1].transition[prev_word[i]] = find_minimized(temp_states[i])
        init_state = find_minimized(temp_states[0])
    return init_state




