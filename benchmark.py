import os
import src.fst as fst
import src.trie as trie
import time
import matplotlib.pyplot as plt
import numpy.random as rand
# ######################################################################################################################
# CONSTRUCTION TIME
# ######################################################################################################################
build_time_list_trie = []
for _ in range(10):
    start = time.time()
    structure = trie.trieBuilder()
    end = time.time()
    build_time_list_trie.append(end - start)
build_time_list_fst = []
n_rep = 10
for _ in range(n_rep):
    start = time.time()
    structure = fst.build_dict_en_fst()
    end = time.time()
    build_time_list_fst.append(end - start)

print('mean time for building trie:', sum(build_time_list_trie)/n_rep, 's')
print('mean time for building fst:', sum(build_time_list_fst)/n_rep, 's')
plt.figure()
plt.boxplot([build_time_list_trie, build_time_list_fst], labels=['trie', 'FST'])
plt.title('structure creation time (s)')
plt.show()

# ######################################################################################################################
# SIZE
# ######################################################################################################################
structure = trie.trieBuilder()
structure.save('trie.pkl')
print('size of trie:', os.path.getsize('trie.pkl'), 'B')
fst.save_fst('fst.pkl')
print('size of fst:', os.path.getsize('fst.pkl'), 'B')

# ######################################################################################################################
# AUTO-COMPLETE
# ######################################################################################################################
# generate query data
query_list = []
with open('data/american-english', 'r') as fp:
    for line in fp:
        line = line.strip()
        if rand.random() < 0.01:  # 1% chance selecting a word ~ 1000 words
            if len(line) > 1:
                line = line[:min(len(line) // 2, 4)]  # words of at most 4 letters
            query_list.append(line)
with open('data/queries', 'w') as fp:
    fp.writelines([w + '\n' for w in query_list])

# autocomplete_times_trie = []
# autocomplete_times_fst = []
autocomplete_answers_trie = []
autocomplete_answers_fst = []
trie_structure = trie.trieBuilder()
fst_structure = fst.build_dict_en_fst()
with open('data/queries', 'r') as fp:
    start = time.time()
    for query in fp:
        query = query.strip()
        res_trie = trie_structure.query(query)
        autocomplete_answers_trie.append(res_trie)
    end = time.time()
    autocomplete_times_trie = end - start
    fp.seek(0)
    start = time.time()
    for query in fp:
        query = query.strip()
        res_fst = fst.fst_prefix_query(query, fst_structure)
        autocomplete_answers_fst.append(res_fst)
    end = time.time()
    autocomplete_times_fst = end - start
    fp.seek(0)
    N_queries = len(fp.readlines())
    print('using', N_queries, 'queries')
print('mean time per query for trie:', autocomplete_times_trie/N_queries, 's')
print('mean time per query for fst:', autocomplete_times_fst/N_queries, 's')

# CHECKING RESULTS COHERENCE
def lists_equal(l1, l2):
    return len(l1) == len(l2) and all([x == y for x,y in zip(sorted(l1), sorted(l2))])
assert all([lists_equal(l1, l2) for l1,l2 in zip(autocomplete_answers_trie, autocomplete_answers_fst)])

# CHECKING DATASET QUALITY
plt.figure()
plt.title('quantity of results per query')
plt.hist([len(l) for l in autocomplete_answers_trie], bins=50)
plt.show()

