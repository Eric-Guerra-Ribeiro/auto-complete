# auto-complete
Auto-complete function using Finite State Transducer (FST), Trie and Levenshtein Automata

## Details on methods implemented

FST and Trie are alternatives for the same task, which consists of:
* receiving a list of words (for FST, this list must be ordered in lexical order, like a natural language dictionary)
* building a compact data structure from this entry that allows for fast query on the original list
* dumping/loading the data structure to/from disk in order to persist it instead of re-building each time

Levenshtein Automata is an automata that allows us to check fast if a query word ``q`` is at Levenshtein distance
(aka edit-distance) at most ``N`` from a reference word ``r``. 
This is an alternative to the more traditional Dynamic Programming algorithm people use for edit-distance.
The automata should be built for each pair (``r``, ``N``) and can then be reused for many queries ``q``.


## The actual auto-complete & its graphical interface

We also have a graphical interface for identifying words with a given prefix, where we can choose between FST or Trie,
or even the Levenshtein Automata to return words with Levenshtein distance at most 1 to the input.
We can combine FST (or Trie) with Levenshtein distance, which is basically the same as returning only the words that are
equal to the query of to the query + some other character in the end.

## References 
FST:
* Mihov, S., Maurel, D. (2001). Direct Construction of Minimal Acyclic Subsequential Transducers. In: Yu, S., Păun, A. (eds) Implementation and Application of Automata. CIAA 2000. Lecture Notes in Computer Science, vol 2088. Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-44674-5_18
* https://blog.burntsushi.net/transducers/ who talks about its FST package in Rust (https://github.com/BurntSushi/fst)
* Indirectly, we also used [Incremental Construction of Minimal Acyclic Finite State Automata and Transducers](https://aclanthology.org/W98-1305) (Daciuk et al., FSMNLP 1998)
  (because Mihov & Maurel (2001) inspire on this paper). Check the blog above to understand the differences between a
  transducer and an automata.

Trie:
* Knowledge from life and https://blog.burntsushi.net/transducers/

Levenshtein Automata:
* https://julesjacobs.com/2015/06/17/disqus-levenshtein-simple-and-fast.html

## Using this code
You are probably interested in the methods/functions:
* ``src.trie.trieBuilder``, ``src.trie.loadTrie``, and ``save`` from the class ``src.trie.Trie``
* all the functions in ``src.fst``
* the class ``src.levenshtein.LevenshteinAutomaton`` and the function ``src.levenshtein.dict_filter_by_levenshtein``
* the module ``src.interface`` that opens the graphical Interface

**NOTE FOR WINDOWS**: Comment-out the line ``window.attributes('-zoomed', True)`` in 
``src.interface`` to avoid a bug you would likely have.