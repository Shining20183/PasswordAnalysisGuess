# 基础分析-密码构成元素分析和结构分析
import re
import os
import collections

class ElementStructAnalysis:
    def analysis(self, run=True, show=False, data='yahoo'):
        # 分析密码，并将分析结果写入文件
        # run: False：不保存分析结果；True：保存分析结果
        # show：True：打印分析结果；False：不打印分析结果
        file_path = "./data/for_analysis/"+data+"_struct.txt"
        if run:
            self.deal_fun_list(data)
        else:
            if not os.path.exists(file_path):
                os.mknod(file_path)
            if not os.path.getsize(file_path):
                print("The "+data+"'s element struct result doesn't get!")

        if show:
            if not os.path.getsize(file_path):
                self.deal_fun_list(data)
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

    def sapmle_deal(self, data):
        # 每次只处理未处理的密码，所以不用删除之前的
        # result_lists = ['struct', 'letter', 'digit', 'symbol']
        # for result_list in result_lists:
        #     with open("./data/for_analysis/"+data+"_"+result_list+".txt", "r+") as fp:
        #         fp.truncate()
        with open("./data/" + data + "_pw_test.txt", "r") as fp:
            for (num, password) in enumerate(fp):
                # 将处理后的密码添加到文件中记录
                with open("./data/"+data+"_pw_done.txt", "a+", encoding="utf-8") as f_done:
                    f_done.write(password)
                password = password.replace("\n", "")
                if password.strip() == "":
                    continue
                pattern1 = re.compile("[a-zA-Z]+")
                letter_strs = re.findall(pattern1, password)
                letter_strs.sort(key=lambda x: len(x), reverse=True)
                print(letter_strs)
                with open("./data/for_analysis/"+data+"_letter.txt", "a", encoding="utf-8")as fp:
                    for letter in letter_strs:
                        fp.write(letter+"\n")

                pattern2 = re.compile("[0-9]+")
                digit_strs = re.findall(pattern2, password)
                digit_strs.sort(key=lambda x: len(x), reverse=True)
                print(digit_strs)
                with open("./data/for_analysis/"+data+"_digit.txt", "a", encoding="utf-8")as fp:
                    for digit in digit_strs:
                        fp.write(digit+"\n")


                symbol_strs = re.findall(r"\W+", password)
                symbol_strs.sort(key=lambda x: len(x), reverse=True)
                print(symbol_strs)
                with open("./data/for_analysis/"+data+"_symbol.txt", "a", encoding="utf-8")as fp:
                    for symbol in symbol_strs:
                        fp.write(symbol+"\n")

                type = self.get_type(password, letter_strs, digit_strs, symbol_strs)
                print("第" + str(num + 1) + "行类型: " + type)
                with open("./data/for_analysis/"+data+"_struct.txt", "a", encoding="utf-8")as fp:
                    fp.write(type+"\n")

    # 计算出现的(结构，数字，字母，特殊字符)次数，并降序存入文件
    def count_dsort(self, data, tp):
        dic = {}
        with open("./data/for_analysis/"+data+"_"+tp+".txt", "r+") as fp:
            result = fp.readlines()
            print(result)
            dic = collections.Counter(result)
            print(sorted(dic.items(), key=lambda x: x[1], reverse=True))
            with open(r'data/for_analysis/' + data + '_' + tp + '_count.txt', 'w', encoding="utf-8") as f:
                for key, value in sorted(dic.items(), key=lambda x: x[1], reverse=True):
                    f.write(key.strip() + "\t" + str(value) + "\n")
            # for line in fp:
            #     line = line.replace("\n", "")
            #     dic = self.insert_strs(dic, [line])
        # d_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        # with open(r'data/for_analysis/' + data + '_' + tp + '_count.txt', 'w', encoding="utf-8") as f:
        #     for value in d_dic:
        #         f.write(value[0] + ": " + str(value[1]) + "\n")

    def deal_fun_list(self,data):
        struct_lists = []
        letter_lists = []
        digit_lists = []
        symbol_lists = []

        with open("./data/" + data + "_pw.txt", "r") as fp:
            for (num, password) in enumerate(fp):
                password = password.replace("\n", "")
                if password.strip() == "":
                    continue
                print("第" + str(num + 1) + "行密码: " + password)

                pattern1 = re.compile("[a-zA-Z]+")
                letter_strs = re.findall(pattern1, password)
                letter_strs.sort(key=lambda x: len(x), reverse=True)
                letter_lists = letter_lists + letter_strs
                # print(letter_lists)

                pattern2 = re.compile("[0-9]+")
                digit_strs = re.findall(pattern2, password)
                digit_strs.sort(key=lambda x: len(x), reverse=True)
                digit_lists = digit_lists + digit_strs
                # print(digit_lists)

                symbol_strs = re.findall(r"\W+", password)
                symbol_strs.sort(key=lambda x: len(x), reverse=True)
                symbol_lists =symbol_lists + symbol_strs
                # print(symbol_lists)

                type = self.get_type(password, letter_strs, digit_strs, symbol_strs)
                print("第" + str(num + 1) + "行类型: " + type)
                struct_lists.append(type)
                print(struct_lists)

        result_lists = ['struct', 'letter', 'digit', 'symbol']
        for result_list in result_lists:
            with open(r'data/for_analysis/' + data + '_' + result_list + '.txt', 'w', encoding="utf-8") as f:
                dic = collections.Counter(eval(result_list+"_lists"))
                print(dic)
                for key, value in sorted(dic.items(), key=lambda x: x[1], reverse=True):
                    f.write(key.strip() + ":\t" + str(value) + "\n")



    def deal_fun(self, data):
        struct_dics = {}
        letter_dics = {}
        digit_dics = {}
        symbol_dics = {}

        with open("./data/" + data + "_pw_test.txt", "r") as fp:
            for (num, password) in enumerate(fp):
                password = password.replace("\n", "")
                if password.strip() == "":
                    continue
                pattern1 = re.compile("[a-zA-Z]+")
                letter_strs = re.findall(pattern1, password)
                letter_dics = self.insert_strs(letter_dics, letter_strs)
                letter_strs.sort(key=lambda x: len(x), reverse=True)
                print(letter_strs)

                pattern2 = re.compile("[0-9]+")
                digit_strs = re.findall(pattern2, password)
                digit_dics = self.insert_strs(digit_dics, digit_strs)
                digit_strs.sort(key=lambda x: len(x), reverse=True)
                print(digit_strs)

                symbol_strs = re.findall(r"\W+", password)
                symbol_dics = self.insert_strs(symbol_dics, symbol_strs)
                symbol_strs.sort(key=lambda x: len(x), reverse=True)
                print(symbol_strs)

                type = self.get_type(password, letter_strs, digit_strs, symbol_strs)
                print("第"+str(num+1)+"行类型: "+type)
                if type not in struct_dics.keys():
                    struct_dics.update({type: 1})
                else:
                    for key, value in struct_dics.items():
                        if key == type:
                            struct_dics[key] = value + 1
        # 存入数据到文件
        result_lists = ['struct', 'letter', 'digit', 'symbol']
        for result_list in result_lists:
            dics = sorted(eval(result_list+"_dics").items(), key=lambda x: x[1], reverse=True)  # 按照字典value降序排列
            # print(struct_dics)  # [('4', 4), ('3', 3), ('2', 2), ('1', 1)]
            with open(r'data/for_analysis/' + data + '_'+result_list+'.txt', 'w', encoding="utf-8") as f:
                for dic in dics:
                    f.write(dic[0] + ": " + str(dic[1]) + "\n")


    # 添加新的字符，数字，特殊字符 串
    def insert_strs(self, dics, strs):
        for str in strs:
            if str not in dics.keys():
                dics.update({str: 1})
            else:
                for key, value in dics.items():
                    if key == str:
                        dics[key] = value + 1
        return dics


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
    datas = ['csdn']
    for data in datas:
        esa.analysis(True, False, data)
        # result_lists = ['struct', 'letter', 'digit', 'symbol']
        # for result_list in result_lists:
        #     esa.count_dsort(data, result_list)