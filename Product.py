#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random
import math
class Product:

    # 类变量定义
    problemArray = []            # 表达式列表表示
    exStr = ''            # 表达式字符串
    answer = 0                   # 答案
    answerStr = ''              # 答案字符串
    operRange = 10                # 操作数范围
    operCount = 3                 # 操作数个数
    decChance = 0                 # 出现分数的概率

    def __init__(self, operRange, operCount, decChance):           #类的构造函数
        self.operRange = operRange
        self.operCount = operCount
        self.decChance = decChance

        result=self.creQues(self.operCount)
        self.problemArray = result['problemArray']
        self.exStr = result['exStr']
        self.answer = result['answer']
        self.answerStr = str(self.DecToStr(result['answer']))

    def creQues(self, count):

        if count == 1:
            oper = self.getOperNum()
            return {
                'problemArray' :    oper['oper'],
                'exStr'    :    oper['operStr'],
                'answer'        :    oper['operArray']
            }
        else:
            leftCount = self.getRandomNum(count-1)
            rightCount = count-leftCount

            left = self.creQues(leftCount)
            right = self.creQues(rightCount)
            operate = self.getRandomNum(4)

            if operate == 4 and right['answer'][0] == 0:
                temp = left
                left = right
                right = temp

            answer = self.calc(left['answer'], right['answer'], operate)

            if answer[0] < 0:
                temp = left
                left = right
                right = temp
                answer = self.calc(left['answer'], right['answer'], operate)

            leftValue = left['answer'][0]/left['answer'][1]
            rightValue = right['answer'][0]/right['answer'][1]

            if (operate == 1 or operate == 3) and leftValue <=rightValue :
                # 当右子树值大于左子树时
                if leftValue < rightValue:
                    problemArray = [right['problemArray'], operate, left['problemArray']]
                #     当左右子树值相等时
                else:
                    # 当左右子树均为树时
                    if (type(left['problemArray']) == list) and (type(right['problemArray']) == list):

                        # 当左子树运算符大于右子树运算符时
                        if left['problemArray'][1] > right['problemArray'][1]:
                            problemArray = [left['problemArray'], operate, right['problemArray']]

                        # 当左子树运算符小于右子树运算符时
                        elif left['problemArray'][1]<right['problemArray'][1]:
                            problemArray = [right['problemArray'], operate, left['problemArray']]

                        # 当左子树运算符等于右子树运算符时
                        else:
                            # 当左子树的左子树小于右子树的左子树时
                            if left['problemArray'][0] < right['problemArray'][0]:
                                problemArray = [right['problemArray'], operate, left['problemArray']]
                            # 当左子树的左子树大于右子树的左子树时
                            elif left['problemArray'][0] > right['problemArray'][0]:
                                problemArray = [left['problemArray'], operate, right['problemArray']]
                            # 当左子树的左子树等于右子树的左子树时
                            else:
                                # 当左子树运算符小于右子树运算符
                                if left['problemArray'][2] < right['problemArray'][2]:
                                    problemArray = [right['problemArray'], operate, left['problemArray']]
                                    problemArray = [left]
                                # 其他情况因概率问题不给予考虑
                                else:
                                    problemArray = [left['problemArray'], operate, right['problemArray']]

                    # 当仅由左子树为树时
                    elif type(left['problemArray']) == list:
                        problemArray = [left['problemArray'], operate, right['problemArray']]
                    # 当仅由右子树为树时
                    elif type(right['problemArray']) == list:
                        problemArray = [right['problemArray'], operate, left['problemArray']]
                    # 当左右子树均为数字，且已有左右子树值相等
                    else:
                        problemArray = [left['problemArray'], operate, right['problemArray']]
            else:
                problemArray = [left['problemArray'], operate, right['problemArray']]


            if type(left['problemArray'])==list and operate in [3,4] and left['problemArray'][1] in [1,2]:
                left['exStr']='('+left['exStr']+')'
            if type(right['problemArray'])==list and not (operate in [1,2] and right['problemArray'][1] in [3,4]):
                right['exStr'] = '(' + right['exStr'] + ')'
            exStr = left['exStr']+self.getOperSymbol(operate)+right['exStr']

            return {
                'problemArray' :    problemArray,
                'exStr'    :    exStr,
                'answer'        :    answer
            }

    def calc(self,operNum1,operNum2,operate):
        '''
        计算值
        :param operNum1: 操作数1
        :param operNum2: 操作数2
        :param operate: 操作
        :return: 计算结果
        '''
        # print("操作数1：",operNum1,"   操作数2",operNum2,"  操作：",self.getOperSymbol(operate))

        if operate == 1:
            fenzi = operNum1[0]*operNum2[1]+operNum2[0]*operNum1[1]
            fenmu = operNum1[1]*operNum2[1]

        elif operate == 2:
            fenzi = operNum1[0]*operNum2[1]-operNum2[0]*operNum1[1]
            fenmu = operNum1[1]*operNum2[1]
            if fenzi < 0:
                return [fenzi, fenmu]
        elif operate == 3:
            fenzi=operNum1[0]*operNum2[0]
            fenmu=operNum1[1]*operNum2[1]

        elif operate == 4:
            fenzi = operNum1[0]*operNum2[1]
            fenmu = operNum1[1]*operNum2[0]

        result=self.stacdardDec(fenzi,fenmu)
        return result

    def getOperNum(self):
        #生成获取操作数，以及是否生成分数随机判断
        operRange=self.operRange
        decChance=self.decChance                                    #遗留问题生成分数的判断decChance放到哪里合适？
        # 将分数出现的概率转换为整形，例：0.5 -> 50
        decChance *= 100
        decChance=int(decChance)
        # 判断是否成功生成操作数
        flag = False

        # 用于存放返回的操作数
        result = {}
        # 若随机生成的100以内的数在概率整形内，则生成分数
        if self.getRandomNum(100) <= decChance :
            operArray = self.getRangeDec()
            result['oper']=operArray[0]/operArray[1]
            result['operStr']=self.DecToStr(operArray)
            result['operArray']=[operArray[0],operArray[1]]
        else:
            oper=self.getRandomNum(operRange)
            result['oper']=oper
            result['operStr']=str(oper)
            result['operArray'] = [oper,1]
        return result

    def DecToStr(self,operArray):
       #分数转化为字符串  带分数
        operNum1 = operArray[0]
        operNum2 = operArray[1]
        if operNum2 == 1:
            return operNum1
        if(operNum1 > operNum2):
            temp = int(operNum1/operNum2)
            operNum1 -= (temp*operNum2)
            return str(temp) + "'" + str(operNum1) + "/" + str(operNum2)
        else:
            return str(operNum1) + "/" + str(operNum2)

    def getRangeDec(self):                     #随机生成分数
        operRange=self.operRange
        while True:
            # 随机生成两个随机数
            operNum1 = self.getRandomNum(operRange)
            operNum2 = self.getRandomNum(operRange)
            # 判断operNum1是否为operNum2的倍数，若是则重新生成随机数
            if (operNum1%operNum2) == 0:
                continue
            # 若operNum1不是operNum2的倍数则已获取到符合要求的 operNum1和 operNum2，退出循环
            else:
                break
        # 将获取到的分子和分母进行化简并返回
        return self.stacdardDec(operNum1, operNum2)

    def stacdardDec(self,operNum1,operNum2):     # 化简分数  接收分子 分母参数
        operNum1FactorList = self.getFactorList(operNum1)
        operNum2FactorList = self.getFactorList(operNum2)
        # 如果分子或分母没有因子的话，则当前分数已经为最简分数
        if len(operNum1FactorList) == 0 or len(operNum1FactorList) == 0:
            return [operNum1, operNum2]
        else:
            # maxFactor用于存储 分子 和 分母 的最大公因子，同时如果循环结束时值仍为-1的话则无最大公因子
            maxFactor = 1
            for operNum1Factor in operNum1FactorList:
                if operNum1Factor in operNum2FactorList:
                    maxFactor = operNum1Factor
            # 若maxFactor已更新，则将分子、分母除以最大公因数即可得到最简分数的分子、分母
            if maxFactor != 1:
                operNum1 = int(operNum1/maxFactor)
                operNum2 = int(operNum2/maxFactor)
            return [operNum1,operNum2]

    def getFactorList(self, oper):   #获取正整数的公因子包括其本身
        l=[]
        for k in range(2, oper+1):
            if (oper % k) == 0:
                l.append(k)
        return l

    def getRandomNum(self, range):
        #获取随机数
        return random.randint(1, range)

    def getOperSymbol(self, operate):
        # 返回1-4位操作符列表形式返回
        operSignArray = ['+', '-', '×', '÷']
        return operSignArray[operate - 1]


