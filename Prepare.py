#import os
from Product import Product
from NIBORLAN import middle_to_after
from NIBORLAN import expression_to_value
from time import sleep
class Prepare:
    # 题目对象数组
    quesList=[]
    # 需要的题目数量
    quesCount = 10
    # 运算数范围
    operRange = 10
    # 操作符个数,当前无参数
    operCount = 3
    # 出现分数的概率
    decChance = 0.5
    #给定的题目文件名
    exercisefile = ''
    #给定的答案文件名
    answerfile = ''

    def __init__(self,argv):
        initSuccess=self.checkArgv(argv)

        if  initSuccess == 0:
            return
        else:
            self.quesList=self.createQuestionList(self.quesCount,self.operRange,self.operCount,self.decChance)
            self.compareResult=self.compareFile(self.exercisefile,self.answerfile)

    #命令行参数判断
    def checkArgv(self, argv):
        i = 0
        while i < len(argv):
            command = argv[i]

            # 设置存储题目数.
            if command == "-n":
                i += 1
                if 0 < int(argv[++i]) and int(argv[++i]) < 99999:
                    self.quesCount = int(argv[++i])
                else:
                    print("命令行-n后的参数",argv[i],"错误")
                    return False

            # 设置题目中运算数范围
            elif command == "-r":
                i += 1
                if 0 < int(argv[++i]) and int(argv[++i]) < 99999:
                    self.operRange = int(argv[++i])
                else:
                    print("命令行-r后的参数",argv[i],"错误")
                    return False

            # 设置题目中运算数个数
            elif command == "-c":
                i += 1
                if 0 < int(argv[++i]) and int(argv[++i]) < 5:
                    self.operCount = int(argv[++i])
                else:
                    print("命令行-c后的参数",argv[i],"错误")
                    return False

            # 设置题目中小数出现的概率
            elif command == "-d":
                i += 1
                if 0 <= float(argv[++i]) and float(argv[++i]) <= 1:
                    self.decChance = float(argv[++i])
                else:
                    print("命令行-d后的参数",argv[i],"错误")
                    return False

            #给定的题目文件exercisefile.txt
            elif command == "-e":
                i += 1
                if( len(argv[++i]) >0 ):
                    self.exercisefile=argv[++i]
                    print(argv[++i])
                else:
                    print("命令行-e后的参数",argv[i],"错误")
                    return False

            #给定的用户文件answerfile.txt
            elif command == "-a":
                i += 1
                if( len(argv[++i]) >0 ):
                    self.answerfile=argv[++i]
                    print(argv[++i])
                else:
                    print("命令行-a后的参数",argv[i],"错误")
                    return False

            i += 1
        return True


    #生成题目
    def createQuestionList(self,count,operRange,operCount,decChance):
        '''
        count: 题目个数
        operRange: 题目操作数范围
        operCount: 题目操作数个数
        decChance: 出现分数的概率
        '''
        qList=[]
        i = 0
        while i < count:
            newQues = Product(operRange,operCount,decChance)
            #调用查重，若重复就在重新初始化一个题目组
            while self.checkRepeat(newQues,qList):
                newQues = Product(operRange, operCount, decChance)

            # 将生成的题目推入数组中
            qList.append({
                "problemArray":newQues.__dict__['problemArray'],
                "exStr":newQues.__dict__['exStr'],
                "answer":newQues.__dict__['answer'],
                "answerStr":newQues.__dict__['answerStr']
            })
            i += 1
        return qList

    #查重
    def checkRepeat(self,newQues,qList):
        problemArray=newQues.__dict__['problemArray']
        for item in qList:
            if problemArray == item['problemArray']:
                return True
        return False

    #返回题目列表
    def getQuestionList(self):
        return self.quesList

    # 对给定问题文件和用户答案文件，对比后得到的分数
    def compareFile(self, efile, afile):
        '''
        efile: 题目文件名
        afile: 答案文件名
        '''
        #题目文件按行读取的列表
        elines = []
        #用户文件按行读取的列表
        alines = []
        #标准答案的列表
        eanswer = []
        #答对的题号列表
        rightList = []
        #答错的题目列表
        wrongList = []

        j = 0
        with open('exercisefile.txt', 'r') as f1:
            elines.append((f1.read().splitlines()))
            print(elines)

        with open('answerfile.txt', 'r') as f2:
            alines.append((f2.read().splitlines()))
            print(alines)

        for eline in elines:
            elineprace = eline
        #标准答案eanswer列表
        for i in elineprace:
            eanswer.append(str(expression_to_value(middle_to_after(str(i)))))
        print(eanswer)
        user=alines[0]
        print(user)
        #统计答案文件的对错情况
        while j < len(eanswer):
            if(eanswer[j] == user[j]):
                rightList.append(j+1)
            else:
                wrongList.append(j+1)
            j += 1
        print(rightList,wrongList)
        return rightList,wrongList


