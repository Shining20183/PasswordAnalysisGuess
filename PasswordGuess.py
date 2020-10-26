# 密码猜测攻击
import sys

import configparser
import time
import re
import csv
from encodings import gb18030
import string
import pandas as pd


from pandas import Series,DataFrame

class PasswdGuess():
    # def __init__(self, passwdList):
    #     self.passwdList = passwdList


    def txt_to_csv(self,file_name):
        csvFile = open("./analysis_result/passwd_analysis/"+file_name+".csv", 'w', newline='', encoding='gb18030')
        writer = csv.writer(csvFile)

        f = open("./analysis_result/struct_analysis/"+file_name+".txt", 'r', encoding='gb18030')
        for line in f:
            line = line.strip('\n')
            csvRow = line.split(':')
            writer.writerow(csvRow)

        f.close()
        csvFile.close()
    def count_strucunit(self):
        dic = {'L1': {}, 'L2': {}, 'L3': {}, 'L4': {}, 'L5': {}, 'L6': {}, 'L7': {}, 'L8': {}, 'L9': {}, 'L10': {},
               'L11': {}, 'L12': {}, 'L13': {}, 'L14': {}, 'L15': {}, 'L16': {}, 'L17': {}, 'L18': {}, 'L19': {},
               'L20': {},
               'D1': {}, 'D2': {}, 'D3': {}, 'D4': {}, 'D5': {}, 'D6': {}, 'D7': {}, 'D8': {}, 'D9': {}, 'D10': {},
               'D11': {}, 'D12': {}, 'D13': {}, 'D14': {}, 'D15': {}, 'D16': {}, 'D17': {}, 'D18': {}, 'D19': {},
               'D20': {},
               'S1': {}, 'S2': {}, 'S3': {}, 'S4': {}, 'S5': {}, 'S6': {}, 'S7': {}, 'S8': {}, 'S9': {}, 'S10': {},
               'S11': {}, 'S12': {}, 'S13': {}, 'S14': {}, 'S15': {}, 'S16': {}, 'S17': {}, 'S18': {}, 'S19': {},
               'S20': {},
               }

        df = DataFrame(columns=('structure', 'nums', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
        structure_l = pd.read_csv('./analysis_result/passwd_analysis/yahoo_letter.csv')
        structure_s = pd.read_csv('./analysis_result/passwd_analysis/yahoo_symbol.csv')
        structure_d = pd.read_csv('./analysis_result/passwd_analysis/yahoo_digit.csv')

        for letter in structure_l:
            line = str(letter[0])
            l = 'L' + str(len(line))
            if line in dic[l]:
                dic[l][line] += 1
            else:
                dic[l][line] = 1
        for symbol in structure_s:
            line = str(symbol[0])
            l = 'S' + str(len(line))
            if line in dic[l]:
                dic[l][line] += 1
            else:
                dic[l][line] = 1
        for digit in structure_d:
            line = str(digit[0])
            l = 'D' + str(len(line))
            if line in dic[l]:
                dic[l][line] += 1
            else:
                dic[l][line] = 1

        with open('str_analysis.csv', 'a', newline='', encoding='gb18030') as f:
            writer = csv.DictWriter(f,fieldnames=)
            writer.writerows(dic)





test=PasswdGuess()
test.txt_to_csv("yahoo_letter")
test.txt_to_csv("yahoo_symbol")
test.txt_to_csv("yahoo_digit")
test.count_strucunit()



# if __name__ == '__main__':
#     test=PasswdGuess()
#     test.txt_to_csv("yahoo_letter")
#     test.txt_to_csv("yahoo_symbol")
#     test.txt_to_csv("yahoo_digit")
#     test.count_strucunit()
#
#     test.txt_to_csv("yahoo_pw")
#     data = pd.read_csv('yahoo.csv', encoding='gb18030')
#     passwdList = pd.Series(data['passwd'].values)



#统计所有结构数量及概率
#得到每种单元结构所有密码形式及数量
#输入yahoo_pw、csdn_pw的csv文件，输出结构统计和单元结构密码词典



#输入结构统计和单元结构密码词典
#得到每一个密码概率，输出按概率排序的密码词典