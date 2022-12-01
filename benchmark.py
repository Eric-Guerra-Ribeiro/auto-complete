import os
import src.fst as fst
import src.trie as trie
import time
import matplotlib.pyplot as plt

# ######################################################################################################################
# CPNSTRUCTION TIME
# ######################################################################################################################
build_time_list_trie = []
for _ in range(3):
    start = time.time()
    structure = trie.trieBuilder()
    end = time.time()
    build_time_list_trie.append(end - start)
build_time_list_fst = []
for _ in range(3):
    start = time.time()
    structure = fst.build_dict_en_fst()
    end = time.time()
    build_time_list_fst.append(end - start)

print(build_time_list_trie)
print(build_time_list_fst)
plt.figure()
plt.boxplot([build_time_list_trie, build_time_list_fst], labels=['trie', 'FST'])
# plt.boxplot(build_time_list_fst)
# plt.title('structure creation time (s)')
# plt.legend(['trie', 'FST'])
plt.show()

# ######################################################################################################################
# SIZE
# ######################################################################################################################
structure = trie.trieBuilder()
structure.save('trie.pkl')
print(os.path.getsize('trie.pkl'))
fst.save_fst('fst.pkl')
print(os.path.getsize('fst.pkl'))
