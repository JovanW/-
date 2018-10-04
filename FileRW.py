import os
from Text import Text
#from Prepare import checkArgv
from Prepare import Prepare
class FileRW:
    # 题目文件名
    exerciseFileNmae=''
    # 题目+答案文件名
    answerFileName=''
    #分数文件名
    resultFileName=''

    def __init__(self):
        self.exerciseFileNmae = 'Exercises.txt'
        self.answerFileName = 'Answers.txt'
        self.resultFileName = 'Result.txt'
        self.compareFileName = 'Grade.txt'

    def outputExercise(self,quesList):
        i=0
        with open(self.exerciseFileNmae, 'w+') as file_object:
            while i<len(quesList):
                file_object.write(str(i+1)+'.'+str(quesList[i]['exStr'])+'=\n')
                i += 1

    def outputAnswer(self,quesList):
        i = 0
        with open(self.answerFileName,'w+') as file_object:
            while i<len(quesList):
                file_object.write(str(i + 1) + "." + str(quesList[i]['exStr']) + '='+ str(quesList[i]['answerStr'])+'\n')
                i += 1

    def outputResult(self,quesList,inputanswer):
        index = 0
        with open(self.resultFileName,'w+') as file_object:
            while index < len(quesList):
                file_object.write(str(index + 1) + "." + str(quesList[index]['exStr']) + '\n')
                file_object.write('Input:' + str(inputanswer[index]))
                file_object.write('     Answer:' + str(quesList[index]['answerStr']))
                if inputanswer[index] == quesList[index]['answerStr']:
                    file_object.write('    Right\n')
                else:
                    file_object.write('    Wrong\n')
                index += 1

    def outputCompare(self,r,w):
        with open(self.compareFileName,'w+') as file_object:
            file_object.write('Correct:'+str(len(r))+'(')
            for i in range(0,len(r)):
                file_object.write(str(r[i])+',')
                i += 1

            file_object.write(')'+'\n')
            file_object.write('Wrong:'+str(len(w))+'(')
            for j in range(0,len(w)):
                file_object.write(str(w[j])+',')
                j += 1
            file_object.write(')')
