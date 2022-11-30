class TrieNode:
      def __init__(self, char: str) -> None:
          self.char = char
          self.end = False
          self.children = {}


class Trie:
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
      
      def dfs(self, node, prefix):
            """Depth-first traversal of the trie
        
            Args:
                  - node: the node to start with
                  - prefix: the current prefix, for tracing a
                  word while traversing the trie
            """
            if node.end:
                  self.output.append(prefix + node.char)
            
            for child in node.children.values():
                  self.dfs(child, prefix + node.char)
      
      def query(self, x):
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

            # Sort the results in reverse order and return
            return sorted(self.output, key=lambda x: x[1], reverse=True)