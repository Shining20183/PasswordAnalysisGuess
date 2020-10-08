# 基础分析-英文单词的使用统计
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

    def analysis2(self, data, run=False, show=True):
        res_filepath = ''
        pw_filepath = ''
        if data == 'csdn':
            res_filepath = 'analysis_result/pinyin_analysis/csdn_pinyin.txt'
            pw_filepath = 'data/csdn_pw.txt'
        elif data == 'yahoo':
            res_filepath = 'analysis_result/pinyin_analysis/yahoo_pinyin.txt'
            pw_filepath = 'data/yahoo_pw.txt'

        if not run:  # 如果不现场运行，直接读取已有文件
            if not os.path.exists(res_filepath):
                print("There is no analysis result, you need set 'run' to True and run again")
        else:
            self.read_re(pw_filepath)
            # 以下是存储运行结果的内容

        if show:
            if not os.path.exists(res_filepath):
                self.read_re(pw_filepath)
            # 以下为从已经存储的数据中读，显示要展示的内容




    def analysis(self, data, save=False, show=True, ):
        # 分析密码，并将分析结果写入文件
        # save: False：不保存分析结果；True：保存分析结果
        # show：True：打印分析结果；False：不打印分析结果
        # data: csdn or yahoo

        wfilepath = ''
        rfilepath = ''
        if data == 'csdn':
            wfilepath = 'analysis_result/pinyin_analysis/csdn_pinyin.txt'
            rfilepath = 'data/csdn_pw.txt'
        elif data == 'yahoo':
            wfilepath = 'analysis_result/pinyin_analysis/yahoo_pinyin.txt'
            rfilepath = 'data/yahoo_pw.txt'

        # 如果选择不保存，则
        if not save:
            pass







        if save:

            self.read_re(rfilepath)
            with open(wfilepath, 'w') as file_obj:
                # 向文件中写入top10的单个拼音
                file_obj.write('========== Top 10 Single Pinyin in ' + data + ' ==========\n')
                mat = "{:15}\t{:15}\t{:15}\t"
                file_obj.write(mat.format('No', 'Pinyin', 'Freq') + 'Upper case\n')
                count = 1
                for item in self.subfreq:
                    line = mat.format(str(count), item[0], str(item[1]))
                    if self.upper.__contains__(item[0]):
                        for item2 in self.upper[item[0]]:
                            line = line + item2[0] + ' '
                    line = line + '\n'
                    file_obj.write(line)
                    count += 1
                    if count > 10:
                        break
                file_obj.write('==============================\n')
                # 向文件中写入top10的一组拼音
                file_obj.write('========== Top 10 Pinyin in ' + data + ' ==========\n')
                mat = "{:15}\t{:15}\t{:15}\t"
                file_obj.write(mat.format('No', 'Pinyin', 'Freq')+'\n')
                count = 1
                for item in self.pinyinfreq:
                    line = mat.format(str(count), item[0], str(item[1])) + '\n'
                    file_obj.write(line)
                    count += 1
                    if count > 10:
                        break


        if show and not save:  # 直接从文件中读取结果
            if data == 'csdn':
                filepath = 'analysis_result/pinyin_analysis/csdn_pinyin.txt'
            elif data == 'yahoo':
                filepath = 'analysis_result/pinyin_analysis/yahoo_pinyin.txt'
            with open(filepath, 'r') as file_obj:
                contents = file_obj.read()
                print(contents)

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
Ana.analysis('yahoo', save=True, show=False)
