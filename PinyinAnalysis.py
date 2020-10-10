# 基础分析-拼音的使用统计
import re
import csv
import os


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


class Pinyin(object):
    def __init__(self, pinyins, tree):
        self.pinyins = pinyins
        # 读入所有有效拼音
        self.tree = tree
        # self.tree = Trie()
        # f = open('data/for_analysis/pinyin_list.txt')
        # for line in f:
        #     self.tree.insert(line.split()[0])
        # f.close()

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
            while end > 0:
                begin = dplink[end]
                result.insert(0, self.pinyins[begin:end])
                end = begin
            return True, result


class PinyinAnalysis:
    def __init__(self):
        self.subfreq = {}
        self.pinyinfreq = {}
        self.upper = {}
        self.tree = Trie()
        f = open('data/for_analysis/pinyin_list.txt')
        for line in f:
            self.tree.insert(line.split()[0])
        f.close()

    def analysis(self, data, run=False, show=True):
        """
        :param data:
        :param run:
        :param show:
        :return:
        """
        res_filepath = ''
        pw_filepath = ''
        if data == 'csdn':
            # res_filepath = 'analysis_result/pinyin_analysis/csdn_pinyin.txt'
            res_filepath = 'analysis_result/pinyin_analysis/csdn/'
            pw_filepath = 'data/csdn_pw.txt'
        elif data == 'yahoo':
            res_filepath = 'analysis_result/pinyin_analysis/yahoo/'
            pw_filepath = 'data/yahoo_pw.txt'

        if not run:  # 如果不现场运行，直接读取已有文件
            if not os.path.exists(res_filepath):
                print("There is no analysis result, you need set 'run' to True and run again")
                return
        else:
            self.run_save(res_filepath, pw_filepath)

        if show:
            if not os.path.exists(res_filepath):
                self.run_save(res_filepath, pw_filepath)
            self.show_res(data, res_filepath)

    def run_save(self, res_filepath, pw_filepath):
        self.read_re(pw_filepath)
        if not os.path.exists(res_filepath):
            os.mkdir(res_filepath)
        with open(res_filepath + 'subfreq.csv', 'w', newline='') as fin:
            csv_writer = csv.writer(fin)
            for item in self.subfreq:
                line = [item[0], item[1]]
                if self.upper.__contains__(item[0]):
                    tmp = ''
                    for item2 in self.upper[item[0]]:
                        tmp = tmp + item2[0] + ':' + str(item2[1]) + ','
                    line.append(tmp)
                csv_writer.writerow(line)
        with open(res_filepath + 'pinfreq.csv', 'w', newline='') as fin:
            csv_writer = csv.writer(fin)
            for item in self.pinyinfreq:
                csv_writer.writerow([item[0], item[1]])

    def show_res(self, data, res_filepath):
        print('========== Top 10 Single Pinyin in ' + data + ' ==========')
        with open(res_filepath + 'subfreq.csv', 'r') as fout:
            reader = csv.reader(fout)
            mat = "{:15}\t{:15}\t{:15}\t"
            print(mat.format('No', 'Pinyin', 'Freq') + 'Upper case')
            num = 1
            for row in reader:
                tmp = mat.format(str(num), row[0], row[1])
                if len(row)==3:
                    tmp +=row[2]
                print(tmp)
                num +=1
                if num>10:
                    break
        print('========== Top 10 Pinyin in ' + data + ' ==========')
        with open(res_filepath + 'pinfreq.csv', 'r') as fout:
            reader = csv.reader(fout)
            mat = "{:15}\t{:15}\t{:15}\t"
            print(mat.format('No', 'Pinyin', 'Freq'))
            num = 1
            for row in reader:
                print(mat.format(str(num), row[0], row[1]))
                num +=1
                if num>10:
                    break

    def sort_dict(self):
        # print('sort_dict')
        self.subfreq = sorted(self.subfreq.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        self.pinyinfreq = sorted(self.pinyinfreq.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        tmpupper = {}
        for key, value in self.upper.items():
            tmpupper[key] = sorted(value.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        self.upper = tmpupper

    def read_re(self, filepath):
        # print('read_re')
        f = open(filepath)
        for line in f:
            line = line.strip('\n')
            pinlist = re.sub('[^a-zA-Z]', ' ', line).split()
            self.count_freq(pinlist)
        self.sort_dict()

    def count_freq(self, pinlist):
        # print('count_freq')
        for pin in pinlist:
            islower = pin.islower()  # True：全都是小写字母
            pinL = pin.lower()
            pinyin = Pinyin(pinL, self.tree)
            res, splitres = pinyin.split()
            if res:  # 如果能拆分为拼音的话
                if self.pinyinfreq.__contains__(pinL):
                    self.pinyinfreq[pinL] += 1
                else:
                    self.pinyinfreq[pinL] = 1
                for i in splitres:
                    if self.subfreq.__contains__(i):
                        self.subfreq[i] += 1
                    else:
                        self.subfreq[i] = 1
                if not islower:  # 如果之前的串中存在大写字母
                    begin = 0
                    end = 0
                    for i in splitres:
                        length = len(i)
                        end = begin + length
                        subpin = pin[begin:end]
                        if not subpin.islower():
                            if self.upper.__contains__(i):
                                if self.upper[i].__contains__(subpin):
                                    self.upper[i][subpin] += 1
                                else:
                                    self.upper[i][subpin] = 1
                            else:
                                self.upper[i] = {subpin: 1}
                        begin = end


Ana = PinyinAnalysis()
Ana.analysis('csdn', run=False, show=True)
