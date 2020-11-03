from tqdm import tqdm
import re
import csv
import gc
import pandas as pd
from pandas import DataFrame
import os


class Analysis(object):
    def __init__(self, passwdList,a):
        self.passwdList = passwdList
        self.a = a

    # 统计每个单元结构所含密码及数量
    def LDSunit(self):
        structure_l = re.compile(r'[A-Za-z]+$')
        structure_d = re.compile(r'\d+$')
        structure_s = re.compile(r'\W+$')
        str_dic = {}  # 单元结构词典
        str_file = open('./analysis_result/passwd_analysis/' + self.a + '_strfile.csv', 'w')
        csv_write = csv.writer(str_file)
        for line in tqdm(self.passwdList, desc='strifile'):  # 将每个密码拆分成单元结构
            letter_list = re.findall(structure_l, str(line))
            digit_list = re.findall(structure_d, str(line))
            sig_list = re.findall(structure_s, str(line))
            for L_str in letter_list:
                tmp_key = 'L' + str(len(L_str))
                if tmp_key in str_dic:
                    if str(L_str) in str_dic[tmp_key]:
                        str_dic[tmp_key][str(L_str)] += 1
                    else:
                        str_dic[tmp_key][str(L_str)] = 1
                else:
                    str_dic[tmp_key] = {str(L_str): 1}  # 行中没有则加上
            for L_str in digit_list:
                tmp_key = 'D' + str(len(str(L_str)))
                if tmp_key in str_dic:
                    if str(L_str) in str_dic[tmp_key]:
                        str_dic[tmp_key][str(L_str)] += 1
                    else:
                        str_dic[tmp_key][str(L_str)] = 1
                else:
                    str_dic[tmp_key] = {str(L_str): 1}
            for L_str in sig_list:
                tmp_key = 'S' + str(len(str(L_str)))
                if tmp_key in str_dic:
                    if str(L_str) in str_dic[tmp_key]:
                        str_dic[tmp_key][str(L_str)] += 1
                    else:
                        str_dic[tmp_key][str(L_str)] = 1
                else:
                    str_dic[tmp_key] = {L_str: 1}
        for tmp_dic in str_dic:
            tpList = sorted(str_dic[tmp_dic].items(), key=lambda item: item[1], reverse=True)  # 将每种单元结构密码按数量排序
            write_res = [tmp_dic]
            for tu in tpList:
                l = str(tu[0]) + '-' + str(tu[1])
                write_res.append(l)  # 得到strifile 即单元结构密码词典
            csv_write.writerow(write_res)

    # 统计密码结构及口令数量
    def passwdStruc(self):
        strucList = []
        for passwd in self.passwdList:  # 将每个密码用DLS表示
            struc = ''
            passwd = str(passwd)
            for ch in passwd:
                if ch.isdigit():
                    struc += 'D'
                elif ch.isalpha():
                    struc += 'L'
                else:
                    struc += 'S'
            strucList.append(struc)

        nums = {}
        for stru in strucList:
            if stru in nums.keys():
                nums[stru] += 1
            else:
                nums[stru] = 1

        # 计算每种结构频率
        df = DataFrame(columns=('structure', 'nums', 'freq'))
        for x in nums.keys():
            ge = '{:.18f}'.format(int(nums[x]) * 1.0 / len(strucList))  # 一种结构数量/密码总数
            df.loc[x] = [x, nums[x], ge]

        # 转换为LxDxSx的形式
        for stri in df['structure']:
            char = stri[0]
            stru = stri[1:]
            c = 1
            res = ''
            for i in stru:
                if i == char:
                    c += 1
                else:
                    res += char
                    res += str(c)
                    char = i
                    c = 1
            res += char
            res += str(c)
            df.loc[stri, 'structure'] = res
        df = df.sort_values(by='nums')
        return df

#生成密码猜测词典（概率前100）
DIC_NUMS = 100
class passwdGuess:
    def __init__(self, structure_df, str_list,a):
        self.structure_df = structure_df
        self.str_list = str_list
        self.a = a

    def PCFG_Pre(self):
        stru_dic = {}
        stru_nums = {}
        for tmp_list in self.str_list:
            tmp_dict = {}
            sums = 0
            for i in range(1, len(tmp_list)):
                str_toparse = tmp_list[i]
                index = re.search(r'-\d+$', str_toparse).span()
                num = int(str_toparse[index[0] + 1:])
                sums += num
                tmp_dict[str_toparse[:index[0]]] = num
            if len(tmp_list)==0:
                continue
            stru_dic[tmp_list[0]] = tmp_dict
            stru_nums[tmp_list[0]] = sums
        return stru_dic, stru_nums

    #计算每个密码概率并排序
    def PCFG_list(self, stru_dic, stru_nums):
        passwd_list = {}
        final_list = {}
        for i in range(len(self.structure_df)):
            passwd_list[self.structure_df.iloc[i][0]] = float(self.structure_df.iloc[i][2])
        result = {}
        cnum = 0
        for key in tqdm(passwd_list, desc='every_passwd_prob'):
            cnum += 1
            parse_list = re.findall(r'[A-Z]\d+', key)
            final_freq = passwd_list[key]
            final_list = {'': final_freq}
            for sub_str in parse_list:
                if stru_dic[sub_str]:
                    lis = sorted(stru_dic[sub_str].items(), key=lambda item: item[1], reverse=True)
                    tmp_dic = {}
                    #依次计算每种结构的所有口令及频率
                    for j in range(int(passwd_list[key] * DIC_NUMS) + 1):
                        if j < len(lis):
                            prob = lis[j][1] * 1.0 / stru_nums[sub_str]
                            # 挨个添加元素并计算此时概率
                            for s in final_list:
                                tmp_dic[lis[j][0] + s] = final_list[s] * prob
                            gc.collect()
                    final_list = tmp_dic  # tmp_dic保存每种密码的概率

            if final_list:
                result[key] = final_list
        result_list = {}
        for k in tqdm(result, desc='to_list'):
            # 二维转为一维 result_list key为每个密码，保存每个密码和其概率
            for r in result[k]:
                result_list[r] = result[k][r]
        res = sorted(result_list.items(),key=lambda item:item[1],reverse=True)
        df = DataFrame(columns=('passwd', 'prob'))
        for q in tqdm(range(DIC_NUMS), desc='to_csv'):
            df.loc[res[q][0]] = [res[q][0], res[q][1]]
        df.to_csv('./analysis_result/passwd_analysis/PasswdGuess_' + self.a + '.csv', encoding = 'gb18030',index=False)

def entrance(a):
    data = pd.read_csv('./analysis_result/passwd_analysis/'+ a +'pw.csv', encoding='gb18030', names=['passwd'])
    passwdList = pd.Series(data['passwd'].values)

    # 统计结构数量并得到单元结构词典
    ana = Analysis(passwdList,a)
    ana.passwdStruc().to_csv('./analysis_result/passwd_analysis/str_analysis_' + a + '.csv', index=False)
    ana.LDSunit()

    # PCFG生成猜测词典
    structure_df = pd.read_csv('./analysis_result/passwd_analysis/str_analysis_' + a + '.csv', encoding='gb18030')
    csv_file = csv.reader(open('./analysis_result/passwd_analysis/' + a + '_strfile.csv'))
    str_list = []
    for i in csv_file:
        str_list.append(i)
    p = passwdGuess(structure_df, str_list,a)
    stru_dic, stru_nums = p.PCFG_Pre()
    p.PCFG_list(stru_dic, stru_nums)

def get_password(run,show,data):
    file_path = "./analysis_result/passwd_analysis/passwdGuess_csdn.csv"
    if data == 'yahoo':file_path = "./analysis_result/passwd_analysis/passwdGuess_yahoo.csv"
    if run:
        entrance(data)
    else:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8"):
                print("新建文件")
        if not os.path.getsize(file_path):
            print("passwdGuess doesn't get!")
    if show:
        if not os.path.getsize(file_path):
            run()
        else:
            pass
    return
if __name__ == '__main__':
    get_password(True,True,'csdn')






