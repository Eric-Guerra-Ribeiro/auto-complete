import os
import src.fst as fst
import src.trie as trie
import time
import matplotlib.pyplot as plt
import numpy.random as rand
# ######################################################################################################################
# CONSTRUCTION TIME
# ######################################################################################################################
n_rep = 10
build_time_list_trie = []
for _ in range(n_rep):
    start = time.time()
    structure = trie.trieBuilder()
    end = time.time()
    build_time_list_trie.append(end - start)
build_time_list_fst = []
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
autocomplete_times_trie = []
autocomplete_times_fst = []
autocomplete_answers_trie = []
autocomplete_answers_fst = []
trie_structure = trie.trieBuilder()
fst_structure = fst.build_dict_en_fst()
N_queries_total = 0
for _ in range(n_rep):
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
    # experiments
    with open('data/queries', 'r') as fp:
        N_queries = len(fp.readlines())
        fp.seek(0)
        start = time.time()
        for query in fp:
            query = query.strip()
            res_trie = trie_structure.query(query)
            autocomplete_answers_trie.append(res_trie)
        end = time.time()
        autocomplete_times_trie.append((end - start) / N_queries)
        fp.seek(0)
        start = time.time()
        for query in fp:
            query = query.strip()
            res_fst = fst.fst_prefix_query(query, fst_structure)
            autocomplete_answers_fst.append(res_fst)
        end = time.time()
        autocomplete_times_fst.append((end - start) / N_queries)
        fp.seek(0)
        N_queries_total += N_queries
print('We used a total of ', N_queries_total, 'queries')
print('mean time per query for trie:', sum(autocomplete_times_trie)/n_rep, 's')
print('mean time per query for fst:', sum(autocomplete_times_fst)/n_rep, 's')

# CHECKING RESULTS COHERENCE
def lists_equal(l1, l2):
    return len(l1) == len(l2) and all([x == y for x,y in zip(sorted(l1), sorted(l2))])
assert all([lists_equal(l1, l2) for l1,l2 in zip(autocomplete_answers_trie, autocomplete_answers_fst)])

# CHECKING DATASET QUALITY
plt.figure()
plt.title('quantity of results per query')
plt.hist([len(l) for l in autocomplete_answers_trie], bins=50)
plt.show()

# BOX PLOT QUERY
plt.figure()
plt.boxplot([autocomplete_times_trie, autocomplete_times_fst], labels=['trie', 'FST'])
plt.title('mean query time (s)')
plt.show()

