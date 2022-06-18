class TrieNode:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.end_here = False
        self.file_path = None
        self.surroundings = []
        self.dictionary = {}
        self.repeats = 0

class Trie:
    def __init__(self):
        self.root = TrieNode(None)
    # def insert(self, word, file_path, surroundings):
    #     parent = self.root
    #     for i, char in enumerate(word):
    #         if char not in parent.children:
    #             parent.children[char] = TrieNode(char)
    #         parent = parent.children[char]
    #         if i == len(word) - 1:
    #             parent.end_here = True
    #             parent.file_path = file_path
    #             parent.surroundings.append(surroundings)
    #             parent.repeats += 1
    #
    #         if file_path in parent.dictionary:
    #             parent.dictionary[file_path].append(surroundings)
    #         else:
    #             parent.dictionary[file_path]=[surroundings]
    def broj_ponavljanja(self, word):
        parent = self.root
        for char in word:
            if char not in parent.children:
                return 0
            parent = parent.children[char]
        return parent.repeats

    def search(self,word):
        self.output = []
        parent = self.root
        for ch in word:
            if ch in parent.children:
                parent = parent.children[ch]
            else:
                return []
        self.dfs(parent,word[:-1])

        return parent.dictionary

    def dfs(self, node, prefix):
        if node.end_here:
            self.output.append((prefix + node.value, node.repeats))
        for child in node.children.values():
            self.dfs(child, prefix + node.value)

    def insert(self, word, file, value):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True

        node.repeats += 1
        if file in node.dictionary:
            node.dictionary[file].append(value)
        else:
            node.dictionary[file] = [value]
