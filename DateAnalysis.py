import os
import re
import matplotlib.pyplot as plt
class DateProcess:
    def __init__(self,oriFileName,resFileName):
        self.oriFileName=oriFileName
        self.ResFileName=resFileName
    # 判断数字串的模式:是普通的数字还是日期性质的数字
    def get_DigitalStr_Pattern(self,digital_str):
        pattern=''
        if len(digital_str)<4: #普通数字
            for index in range(len(digital_str)):
                pattern+='D'
                return pattern
        elif len(digital_str)>=4:
            if re.search(r'1[7-9]\d{2}|2[0-1]\d{2}',digital_str):
                return 'yyyy'
            if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])',digital_str):
                return 'yyyymm'
            if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',digital_str):
                return 'yyyymmdd'
            if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])(1[7-9]\d{2}|2[0-1]\d{2})', digital_str):
                return 'mmddyyyy'
            if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])(1[7-9]\d{2}|2[0-1]\d{2})', digital_str):
                return 'ddmmyyyy'
            if re.search(r'[0-9][0-9](0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', digital_str):
                return 'yymmdd'
            if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[0-9][0-9]', digital_str):
                return  'mmddyy'
            if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])[0-9][0-9]', digital_str):
                return 'ddmmyy'
            if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])',digital_str):
                return 'mmdd'
            else:
                for index in range(len(digital_str)):
                    pattern += 'D'
                    return pattern

    #从字典中获取仅包含日期的模式:LLDDSSyyddmm->yyddmm
    def getDatePatternOnly2(self,resultDict):
        res_dict=dict()
        for key,value in resultDict.items():
            if (key.find('y')>=0) or (key.find('m')>=0) or (key.find('d')>=0):
                res_dict[key]=value
        return res_dict
    def getDatePatternOnly(self,data_list):
        res_dict=dict()
        res_dict['yyyymm']=0
        res_dict['yyyymmdd']=0
        res_dict['yyyy']=0
        res_dict['mmddyyyy']=0
        res_dict['ddmmyyyy']=0
        res_dict['yymmdd']=0
        res_dict['mmdd']=0
        res_dict['ddmmyy']=0
        res_dict['mmddyy']=0
        for item in data_list:
            if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])', item):
                res_dict['yyyymm'] += 1
            if re.search(r'(1[7-9]\d{2}|2[0-1]\d{2})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', item):
                res_dict['yyyymmdd'] += 1
            if re.search(r'1[7-9]\d{2}|2[0-1]\d{2}', item):
                res_dict['yyyy'] += 1
            if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])(1[7-9]\d{2}|2[0-1]\d{2})', item):
                res_dict['mmddyyyy'] += 1
            if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])(1[7-9]\d{2}|2[0-1]\d{2})', item):
                res_dict['ddmmyyyy'] += 1
            if re.search(r'[0-9][0-9](0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', item):
                res_dict['yymmdd'] += 1
            if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])', item):
                res_dict['mmdd'] += 1
            if re.search(r'(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[0-9][0-9]', item):
                res_dict['mmddyy'] += 1
            if re.search(r'(0[1-9]|[1-2][0-9]|3[0-1])(0[1-9]|1[0-2])[0-9][0-9]', item):
                res_dict['ddmmyy'] += 1
        return res_dict

    # 获取整个字符串的模式，并对相同模式串进行统计
    def get_WholeStr_Pattern(self,oriFileName,resFileName):
        result_dict=dict()
        with open(oriFileName,'r',encoding='ISO--8859-1') as readFileObj:
                date_list=readFileObj.readlines()
                for date_item in date_list:
                       #将数字提取出来，判断是否是日期
                       result_pattern=''#整个串的模式，如A(字母)+d(普通数字)+YY(年)DD(日)MM(月)+S(其它字符)
                       digital_str=''#数字串
                       end_pos=0
                       index=0
                       while index<len(date_item):
                           end_pos=index
                           if date_item[index].isdigit():  # 获取其后面的所有数字
                               for index_from in range(index, len(date_item)):
                                   if date_item[index_from].isdigit():
                                       digital_str += date_item[index_from]
                                   else:
                                       end_pos=index_from
                                       break
                               pattern = self.get_DigitalStr_Pattern(digital_str)
                               pattern=str(pattern)
                               result_pattern += pattern
                           elif date_item[index].isalpha():
                               result_pattern += 'L'
                           else:
                               result_pattern += 'S'
                           if end_pos!=index:
                               index=end_pos
                           else:
                               index+=1
                       if result_pattern not in result_dict.keys() and result_pattern is not None:
                           result_dict[result_pattern]=1
                       elif result_pattern in result_dict.keys() and result_pattern is not None:
                           result_dict[result_pattern] = result_dict[result_pattern] + 1
                #将字符串模式统计结果写入文件中,按照值降序排序
                result_dict_list=sorted(result_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
                with open(resFileName+'_all_pattern.txt','w',encoding='ISO--8859-1') as writeFileObj:
                    for items in result_dict_list:
                        writeFileObj.write(str(items)+'\n')
                # 选取仅包含日期类型的结果写入文件中
                result_dict2 = self.getDatePatternOnly(date_list)
                result_dict_list = sorted(result_dict2.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
                with open(resFileName+'_only_date_pattern.txt','w',encoding='ISO--8859-1') as writeFileObj:
                    for items in result_dict_list:
                        writeFileObj.write(str(items)+'\n')

class DateAnalysis:
    def analysis(self, data, run=False, show=True):
        # 分析密码，并将分析结果写入文件
        # save: False：不保存分析结果；True：保存分析结果
        # show：True：打印分析结果；False：不打印分析结果
        # data: csdn or yahoo
        orifilepath=''
        resfilepath=''
        if data=='yahoo':
            orifilepath='data/yahoo_pw.txt'
            resfilepath='analysis_result/date_analysis/yahoo_date'
        elif data=='csdn':
            orifilepath = 'data/csdn_pw.txt'
            resfilepath = 'analysis_result/date_analysis/csdn_date'
        date_process=DateProcess(orifilepath,resfilepath)
        if not run:
            # 不存在分析结果文件
            if not os.path.exists(resfilepath+'_only_date_pattern.txt'):
                print("There are no analysis results! You need to set 'run' to be True and run again.")
            else:
                # 存在分析结果文件，但分析文件内容为空
                with open(resfilepath+'_only_date_pattern.txt','r') as readFileObj:
                    file_list=readFileObj.readlines()
                    if len(file_list)<1:
                        print("There exists analysis result file.But there is no content.Run again and check it?")
        else:
            # 运行密码分析函数，将结果存储在对应的文件中
            date_process.get_WholeStr_Pattern(orifilepath,resfilepath)
        if show:
            # 检查是否存在分析结果，如果不存在，运行密码分析函数，并将结果存储在文件中
            if not os.path.exists(resfilepath+'_only_date_pattern.txt'):
                date_process.get_WholeStr_Pattern(orifilepath, resfilepath)
            else: # 存在分析结果文件
                with open(resfilepath+'_only_date_pattern.txt','r',encoding='ISO--8859-1') as readFileObj:
                    file_list=readFileObj.readlines()
                    if len(file_list)<1:
                        date_process.get_WholeStr_Pattern(orifilepath, resfilepath)
                        # 分析结果文件内容为空,执行密码分析函数，将结果存储在文件中

            # 将top10最常用的日期匹配模式打印在控制台中
            with open(resfilepath+'_only_date_pattern.txt', "r",encoding='ISO--8859-1') as fileObj:
                content = fileObj.readlines()
                counts=0
                print('========================='+data+' datasets analysis result shows=========================')
                for iter in content:
                    if counts>9:
                        break
                    print(iter,end='')
                    counts += 1
    def visual(self,data):
        if data == 'yahoo':
            orifilepath = 'data/yahoo_pw.txt'
            resfilepath = 'analysis_result/date_analysis/yahoo_date'
        elif data == 'csdn':
            orifilepath = 'data/csdn_pw.txt'
            resfilepath = 'analysis_result/date_analysis/csdn_date'
        date_process=DateProcess(orifilepath,resfilepath)
        if not os.path.exists(resfilepath+'_only_date_pattern.txt'):
            date_process.get_WholeStr_Pattern(orifilepath, resfilepath)
        #读取文件开始画图
        self.draw(data,resfilepath+'_only_date_pattern.txt')
    #画图
    def draw(self,data,filePath):
        with open(filePath,'r') as readObj:
            content_list=readObj.readlines()
            key_list = []
            value_list = []
            counts=0
            for iter in content_list:
                if counts > 9:
                    break
                iter = iter.replace('(', '').replace(')', '').replace('\'', '')
                split_key = iter.split(',')
                key_list.append(split_key[0].strip())
                value_list.append(float(split_key[1].strip()))
                counts += 1
            explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
            plt.figure(figsize=(8, 6))
            plt.pie(value_list, labels=key_list, explode=explode, startangle=60, autopct='%1.1f%%')
            plt.title(data + ' datasets date password statistics')
            plt.show()

# if __name__=='__main__':
#     date_ana=DateAnalysis()
#     date_ana.analysis('yahoo',run=True,show=True)
#     date_ana.analysis('csdn',run=True,show=True)
#     date_ana.visual('csdn')
#     date_ana.visual('yahoo')
