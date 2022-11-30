import pickle
class TrieNode:
      """
      A Node in the Trie.
      """
      def __init__(self, char: str) -> None:
          self.char = char
          self.end = False # Flag to mark if a word ends in the node
          self.children = {} # Dict of node's children


class Trie:
      """
      Trie class.
      """
      def __init__(self) -> None:
          self.root = TrieNode("")
      
      def insert(self, word: str):
            node = self.root

            # Loop through each character in the word
            # Check if there is no child containing the character, create a new child for the current node
            for char in word:
                  if char in node.children:
                        node = node.children[char]
                  else:
                        # If a character is not found,
                        # create a new node in the trie
                        new_node = TrieNode(char)
                        node.children[char] = new_node
                        node = new_node
        
            # Mark the end of a word
            node.end = True
      
      def dfs(self, node: TrieNode, prefix: str):
            """Depth-first traversal of the trie
        
            Args:
                  - node: the node to start with
                  - prefix: the current prefix, for tracing a word while traversing the trie
            """
            if node.end:
                  self.output.append(prefix + node.char)
            
            for child in node.children.values():
                  self.dfs(child, prefix + node.char)
      
      def query(self, x: str):
            """Given an input (a prefix), retrieve all words stored in
            the trie with that prefix, sort the words by the number of 
            times they have been inserted
            """
            # Use a variable within the class to keep all possible outputs
            # As there can be more than one word with such prefix
            self.output = []
            node = self.root
            
            # Check if the prefix is in the trie
            for char in x:
                  if char in node.children:
                        node = node.children[char]
                  else:
                        # cannot found the prefix, return empty list
                        return []
            
            # Traverse the trie to get all candidates
            self.dfs(node, x[:-1])

            # Sort the results and return
            return sorted(self.output)
      
      def save(self, path : str ='trie.pkl'):
            filehandler = open(path, 'wb')
            pickle.dump(self, filehandler)

def trieBuilder() -> Trie:
      """
      Trie builder for Linux's dictionary.
      """
      trie = Trie()
      with open('data/american-english', 'r') as f:
            lines = f.readlines()
            for word in lines:
                  trie.insert(word.strip())
      return trie

def loadTrie(path: str) -> Trie:
      """
      Loads a Trie saved in pickle format.
      """
      filehandler = open(path, 'rb')
      return pickle.load(filehandler)