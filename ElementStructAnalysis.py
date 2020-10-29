# 基础分析-密码构成元素分析和结构分析
import re
import os
import collections
from tqdm import tqdm

class ElementStructAnalysis:

    def __init__(self):
        self.pattern1 = re.compile("[a-zA-Z]+")
        self.pattern2 = re.compile("[0-9]+")

    def analysis(self, run, show, data):
        # 分析密码，并将分析结果写入文件
        # run: False：不保存分析结果；True：保存分析结果
        # show：True：打印分析结果；False：不打印分析结果
        file_path = "./analysis_result/struct_analysis/"+data+"/"+data+"_struct.txt"
        if run:
            self.deal_fun(data)
        else:
            if not os.path.exists(file_path):
                with open(file_path, "w",encoding="utf-8"):
                    print("新建文件")
            if not os.path.getsize(file_path):
                print("The "+data+"'s element struct result doesn't get!")

        if show:
            if not os.path.getsize(file_path):
                self.deal_fun(data)
            with open(file_path, "r") as fp:
                deal_results = fp.readlines()
                print_len = 10
                if len(deal_results) < 10:
                    print_len = len(deal_results)
                for i in range(0, print_len):
                    print(deal_results[i].strip())
        else:
            pass
        return

    # 处理方法
    def deal_fun(self,data):
        struct_lists = []
        letter_lists = []
        digit_lists = []
        symbol_lists = []

        with open("./data/" + data + "_pw.txt", "r") as fp:
            c=fp.read().split('\n')
            pbar=tqdm(total=len(c))
            for password in c:
                password = password.replace("\n", "")
                if password.strip() == "":
                    continue

                letter_strs = re.findall(self.pattern1, password)
                letter_strs.sort(key=lambda x: len(x), reverse=True)
                letter_lists.extend(letter_strs)

                digit_strs = re.findall(self.pattern2, password)
                digit_strs.sort(key=lambda x: len(x), reverse=True)
                digit_lists.extend(digit_strs)

                symbol_strs = re.findall(r"\W+", password)
                symbol_strs.sort(key=lambda x: len(x), reverse=True)
                symbol_lists.extend(symbol_strs)

                type = self.get_type(password, letter_strs, digit_strs, symbol_strs)
                struct_lists.append(type)
                pbar.update(1)
            pbar.close()

        result_lists = ['struct', 'letter', 'digit', 'symbol']
        for result_list in result_lists:
            with open(r'analysis_result/struct_analysis/' + data+"/" +data+ '_' + result_list + '.txt', 'w', encoding="utf-8") as f:
                dic = collections.Counter(eval(result_list+"_lists"))
                print(dic)
                for key, value in sorted(dic.items(), key=lambda x: x[1], reverse=True):
                    f.write(key.strip() + ": " + str(value) + "\n")


    # 获得口令的结构类型
    def get_type(self, passwd="Mnab33M1Mn!tTLs", letter_strs= ["Mnab","tTLs","Mn","M"], digit_strs= ['1',"33"], symbls_strs= ['!'] ):
        type = ""
        dic = {}
        dic.update(self.get_lgs_local("L", letter_strs, passwd))
        dic.update(self.get_lgs_local("D", digit_strs, passwd))
        dic.update(self.get_lgs_local("S", symbls_strs, passwd))
        # print(dic)
        dic = sorted(dic.items(), key=lambda x: x[0])
        # print(dic)
        for d in dic:
            type = type + d[1]
        # print(type)
        return type

    # 获得子母串，数字串， 特殊字符串的位置
    def get_lgs_local(self, t, lists, passwd):
        temp_dic = {}
        for list in lists:
            length = len(list)
            local = self.indexstr(passwd, list)
            val = t+str(length)
            for l in local:
                if l not in temp_dic.keys():
                    temp_dic.update({l: val})
        return temp_dic

    # 查找指定字符串str1包含指定子字符串str2的全部位置， 以列表形式返回
    def indexstr(self, str1, str2):

        lenth2 = len(str2)
        lenth1 = len(str1)
        indexstr2 = []
        i = 0
        while str2 in str1[i:]:
            indextmp = str1.index(str2, i, lenth1)
            indexstr2.append(indextmp)
            i = (indextmp + lenth2)
        return indexstr2



if __name__ == '__main__':
    esa = ElementStructAnalysis()
    datas = ['csdn', 'yahoo']
    for data in datas:
        esa.analysis(True, True, data)
