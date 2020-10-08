# 基础分析-英文单词的使用统计


class Node(object):
    def __init__(self):
        self.word = None
        self.children = {}


class Trie(object):
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word

    def find(self, word):
        node = self.root
        res = False
        for c in word:
            if c not in node.children:
                return res
            node = node.children[c]
        if node.word:
            return True
        else:
            return False

    def find_initial_with(self, prefix_word):
        node = self.root
        for c in prefix_word:
            if c not in node.children:
                return False
            node = node.children[c]
        if not node:
            return False
        return True

    def delete(self, word, node=None, i=0):
        node = node if node else self.root
        c = word[i]
        if c in node.children:
            child_node = node.children[c]
            if len(word) == (i + 1):
                return node.children.pop(c) if len(child_node.children) == 0 else False
            elif self.delete(word, child_node, i + 1):
                return node.children.pop(c) if (len(child_node.children) == 0 and not child_node.word) else False
        return False

    def __collect_words(self, node):
        results = []
        if node.word:
            results.append(node.word)
        for k, v in node.children.iteritems():
            results.extend(self.__collect_words(v))
        return results

    def get_initial_with(self, prefix_word):
        node = self.root
        for c in prefix_word:
            if c not in node.children:
                return []
            node = node.children[c]

        return self.__collect_words(node)

class pinyin(object):
    def __init__(self, pinyins):
        self.pinyins = pinyins
        # 读入所有有效拼音
        self.tree = Trie()
        # f = open('pinyin/pinyin_list.txt')
        f = open('pinyin_list.txt')
        for line in f:
            self.tree.insert(line.split()[0])
        f.close()

    def split(self):
        n = len(self.pinyins)
        dp = [False] * (n + 1)
        dplink = [-1] * (n + 1)
        dp[0] = True
        for i in range(n):
            for j in range(i + 1, n + 1):
            # for j in range(n, i , -1):
                if dp[i] and self.tree.find(self.pinyins[i:j]):
                    if not dp[j]:
                        dplink[j] = i
                    dp[j] = True

        if not dp[-1]:
            return False, None
        else:
            result = []
            end = n
            while end>0:
                begin = dplink[end]
                result.insert(0,self.pinyins[begin:end])
                end = begin
            return True,result



class PinyinAnalysis:
    def analysis(self, save = False, show = True):
        # 分析密码，并将分析结果写入文件
        # save: False：不保存分析结果；True：保存分析结果
        # show：True：打印分析结果；False：不打印分析结果
        pass