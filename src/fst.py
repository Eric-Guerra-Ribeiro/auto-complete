from typing import Union
import json


class State:
    def __init__(self):
        self.final: Union[bool, None] = None
        self.transition = {}
        self.output_set: Union[set, None] = {""}  # for final states only TODO THIS IS NOT NEEDED IN OUR APPLICATION !!
        self.transition_output = {}

    def clear(self):
        self.final = False
        self.transition = {}
        # TODO do we need to clear output_set or transition_output as well? Not clear in paper...
        # self.output_set = {""}
        # self.transition_output.clear()

    def one_level_copy(self):
        # in the code for creating the FST we need to copy a state, but in a "not totally recursive" way (no deepcopy)
        # or FST will look actually like a trie/prefix-tree because of the deep states we would accidentally duplicate
        new_state = State()
        new_state.final = self.final
        new_state.transition = self.transition
        new_state.output_set = self.output_set
        new_state.transition_output = self.transition_output
        return new_state

    def recursive_print(self, node_name='START', out=None, level=0):
        print('-' * level, node_name, '/' + str(out) if out else '', '-', self)
        for char, child in self.transition.items():
            child.recursive_print(node_name=char,
                                  out=self.transition_output[char] if char in self.transition_output else None,
                                  level=level + 1)


def create_fst(fp):
    mtsd = {}  # MinimumTransducerStatesDictionary
    MAX_WORDS_SZ = 23  # "electroencephalograph's"

    def find_minimized(s: State):
        """returns an equivalent state from the dict.
         If not present inserts a copy of the parameter to the dictionary and returns it
        """
        hashed = json.dumps(s, default=lambda o: o.__dict__ if isinstance(o, dict) or isinstance(o, State) else list(o), sort_keys=True)  # TODO Hash s (should be invariant to permutation)
        if hashed not in mtsd:
            r = s.one_level_copy()
            mtsd[hashed] = r
            return r
        return mtsd[hashed]

    temp_states = []  # FST is a DAG, and this variable holds the current working "branch"
    for _ in range(MAX_WORDS_SZ + 1):
        temp_states.append(State())
    prev_word = ''
    temp_states[0].clear()
    with open(fp, 'r') as f:
        for curr_out, curr_word in enumerate(f):  # we are considering the OUTPUT as the WORD POSITION in the input file
            curr_word = curr_word.strip()
            # Compute longest common prefix of current and previous words:
            prefixlenp1 = 1
            while prefixlenp1 < len(curr_word) and prefixlenp1 < len(prev_word) and\
                    prev_word[prefixlenp1-1] == curr_word[prefixlenp1-1]:
                prefixlenp1 += 1
            # Minimize the states from the suffix of previous word
            # (in terms of https://blog.burntsushi.net/transducers, this means combining existing frozen states to the
            # previous word suffix, which we will know we can now freeze)
            for i in range(len(prev_word), prefixlenp1 - 1, -1):
                temp_states[i-1].transition[prev_word[i-1]] = find_minimized(temp_states[i])
            # Init tail states for current word:
            for i in range(prefixlenp1, len(curr_word) + 1): # TODO pode ser simplificado para temp_states[i-1].transition[curr_word[i-1]] = State() fazendo final=False por init??
                temp_states[i].clear()
                temp_states[i-1].transition[curr_word[i-1]] = temp_states[i]
            if curr_word != prev_word:
                temp_states[len(curr_word)].final = True
                temp_states[len(curr_word)].output_set = {''}
            for j in range(1, prefixlenp1):
                out = temp_states[j-1].transition_output[curr_word[j-1]]
                common_prefix = min(out, curr_out)  # XXX REMARK in our application, transition outputs are simply ints
                # so their "prefix" is the min function (as mentioned in https://blog.burntsushi.net/transducers)
                word_suffix = out - common_prefix
                temp_states[j-1].transition_output[curr_word[j-1]] = common_prefix
                # "push right" the difference between out and min(out, curr_out)
                for c in temp_states[j].transition.keys():
                    new_out = word_suffix + temp_states[j].transition_output[c] \
                        if c in temp_states[j].transition_output else word_suffix
                    temp_states[j].transition_output[c] = new_out
                if temp_states[j].final:
                    temp_states[j].output_set = set([word_suffix + t for t in temp_states[j].output_set])
                curr_out -= common_prefix
            if curr_word == prev_word:
                if len(temp_states[len(curr_word)].output_set) == 1 and '' in temp_states[len(curr_word)].output_set:
                    temp_states[len(curr_word)].output_set = {curr_out}
                else:
                    temp_states[len(curr_word)].output_set.add(curr_out)
            else:
                temp_states[prefixlenp1-1].transition_output[curr_word[prefixlenp1-1]] = curr_out
            prev_word = curr_word
        # Minimize the states of the LAST word:
        for i in range(len(curr_word), 0, -1):
            temp_states[i-1].transition[prev_word[i-1]] = find_minimized(temp_states[i])
        init_state = find_minimized(temp_states[0])
    return init_state


if __name__ == '__main__':
    import tempfile
    import os
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.writelines([b'mon\n', b'thurs\n', b'tues\n'])
    fp.seek(0)
    FST = create_fst(fp.name)
    FST.recursive_print()
    fp.close()
    os.unlink(fp.name)
    print()
    # ------------------------------------------------------------------------------------------------------------------
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.writelines([b'mon\n', b'thurs\n', b'thurs\n', b'tues\n'])  # FIXME some suffixes not merged in this corner case
    fp.seek(0)
    FST = create_fst(fp.name)
    FST.recursive_print()
    fp.close()
    os.unlink(fp.name)
    print()
    # ------------------------------------------------------------------------------------------------------------------
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.writelines([b'mon\n', b'thurs\n', b'tues\n', b'tye\n'])
    fp.seek(0)
    FST = create_fst(fp.name)
    FST.recursive_print()
    fp.close()
    os.unlink(fp.name)
    print()

