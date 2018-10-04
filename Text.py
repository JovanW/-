#import sys
class Text:
    # 当前测试对象所使用的题目列表
    quesList=[]

    # 答题正确题目对应的题号
    correctArray = []

    # 答题错误题目对应的题号
    wrongArray = []

    # 用户输入的答案数组
    inputAnswer = []

    def __init__(self,quesList):
        # quesList:初始化
        self.quesList=quesList

    def begin(self):
        '''
        开始答题，循环输出并等待用户输入答案
        '''
        qlist=self.quesList
        i=0
        self.inputAnswer=[]

        while i < len(qlist):
            item = qlist[i]
            inputAnswer = input('Question ' + str(i + 1) + "：\n" + str(item['exStr']) + '=')
            self.inputAnswer.append(inputAnswer)
            if str(inputAnswer)==str(item['answerStr']):
                print ('Correct\n')
                self.correctArray.append(i+1)
            else:
                print ('Wrong，The correct answer is：',item['answerStr'],'\n')
                self.wrongArray.append(i+1)
            i += 1
        return

    def printResult(self):
        print ('Result：')
        print ('  Correct:',len(self.correctArray),self.correctArray)
        print ('  Wrong:',len(self.wrongArray),self.wrongArray)