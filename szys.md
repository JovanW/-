# 一.项目信息
　项目成员：夏翔  韦智锋

　项目地址： [https://github.com/Steven-MJ/ITEM](https://github.com/Steven-MJ/ITEM "Github")

　实现一个自动生成小学四则运算题目的命令行程序。

需求：

1.使用 -n 参数控制生成题目的个数，例如

	Myapp.exe -n 10		
	
将生成10个题目。

2.使用 -r 参数控制题目中数值（自然数、真分数和真分数分母）的范围，例如
	Myapp.exe -r 10

将生成10以内（不包括10）的四则运算题目。该参数可以设置为1或其他自然数。该参数必须给定，否则程序报错并给出帮助信息。

3.生成的题目中计算过程不能产生负数，也就是说算术表达式中如果存在形如e1 − e2的子表达式，那么e1 ≥ e2。

4.生成的题目中如果存在形如e1 ÷ e2的子表达式，那么其结果应是真分数。

5.每道题目中出现的运算符个数不超过3个。

6.程序一次运行生成的题目不能重复，即任何两道题目不能通过有限次交换+和×左右的算术表达式变换为同一道题目。例如，23 + 45 = 和45 + 23 = 是重复的题目，6 × 8 = 和8 × 6 = 也是重复的题目。3+(2+1)和1+2+3这两个题目是重复的，由于+是左结合的，1+2+3等价于(1+2)+3，也就是3+(1+2)，也就是3+(2+1)。但是1+2+3和3+2+1是不重复的两道题，因为1+2+3等价于(1+2)+3，而3+2+1等价于(3+2)+1，它们之间不能通过有限次交换变成同一个题目。

生成的题目存入执行程序的当前目录下的Exercises.txt文件，格式如下：

	1. 四则运算题目1
	2. 四则运算题目2
	……

其中真分数在输入输出时采用如下格式，真分数五分之三表示为3/5，真分数二又八分之三表示为2’3/8。

7.在生成题目的同时，计算出所有题目的答案，并存入执行程序的当前目录下的Answers.txt文件，格式如下：

	1. 答案1
	2. 答案2

特别的，真分数的运算如下例所示：1/6 + 1/8 = 7/24。

8.程序应能支持一万道题目的生成。

9.程序支持对给定的题目文件和答案文件，判定答案中的对错并进行数量统计，输入参数如下：
 
	Myapp.exe -e <exercisefile>.txt -a <answerfile>.txt
 
统计结果输出到文件Grade.txt，格式如下：
 
	Correct: 5 (1, 3, 5, 7, 9)
	Wrong: 5 (2, 4, 6, 8, 10)

其中“:”后面的数字5表示对/错的题目的数量，括号内的是对/错题目的编号。为简单起见，假设输入的题目都是按照顺序编号的符合规范的题目。

#二.PSP
PSP2.1	Personal|Software Process Stages |预估耗时（分钟）|实际耗时（分钟）
---- |--- |--- | ----
Planning|计划|													 	20|20
Estimate| 估计这个任务需要多少时间| 								 	20|20
Development|开发	|													1070|1005
Analysis| 需求分析 (包括学习新技术)|								60|40
 Design Spec| 生成设计文档|											40|40
 Design Review| 设计复审 (和同事审核设计文档)	|						30|40
 Coding Standard| 代码规范 (为目前的开发制定合适的规范)|				30|30
 Design| 具体设计  |												60|45
 Coding| 具体编码  |												400|360
 Code Review| 代码复审	|											30|25
 Test| 测试（自我测试，修改代码，提交修改）|							200|150
Reporting|报告	|													120|150
 Test Report| 测试报告	|											30|25
 Size Measurement| 计算工作量|										30|20
 Postmortem & Process Improvement Plan| 事后总结, 并提出过程改进计划|		30|40	
合计  |   |	

#三.设计实现思路及实现过程

- 当我构思这个项目时，我的想法是一个再复杂的表达式最终也会是，两个操作数一个操作符构成，由简至繁，令我有了递归的想法通过递归嵌套的方式来实现表达式的生成，而其存储结构，由两个操作数一个操作符至底向上递归这一特点加上google搜索到的资料，决定使用二叉树结构。

- 关于计算表达式结果这一点，我思考以及两人讨论后，至底向上递归生成表达式，一边生成一边计算，且无论整数、分数都以[分子，分母]的形式参与计算，整数的分母则为1。最终四则运算均变成分数间的运算，保持计算的一致性。

- 关于查重这一部分，参考过得资料大多是根据中缀表达式--->后缀表达式--->二叉树----->二叉树比较判重，由于递归至底向上生成的特殊性，运算表达式重复的发生无外乎是交换律所引起的，因此在生成表达式的过程中设定了几个判定条件使其避免交换律的发生，从而避免重复表达式的产生。

- 关于检查答案这一块，需要对传进来的表达式进行计算得到的标准答案与用户答案进行比对，这一块因为我写在递归里的计算函数没有办法使用，需要写一个方法，于是最先是实现了在命令行里进行用户输入所生成题目答案，最后与标准答案进行判断正误。于9.29日还是决定尝试用逆波兰表达式中缀转后缀计算表达式结果接收题目文件并对用户答案进行检查。

###项目文件结构
- Main.py           主函数
- Product.py       表达式生成、计算答案、表达式的查重
- Prepare.py       命令行参数所对应相应的功能
- FileRW.py         文件操作
- NIBORLAN.py 逆波兰表达式函数中缀转后缀计算结果  
- Text.py              用户所输入生成题目的答案的检查正误并输出文件
　　
###二叉树结构：
![](https://i.imgur.com/BNf5dHz.png)
#四.关键代码说明
表达式的结果，表达式，二叉树结构均在递归过程中同步产生，递归结束所需要结果均已完成。当前操作数不为1进入递归直至递归至叶子节点产生相应操作数，当遇到除法且右子为0，以及子树计算结果为负则进行左右子树交换。最终得到左右
子树相对应的值

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
　　　　

查重，上述设计思路已经说过查重部分通过以下几种判定条件避免产生交换律而发生重复题目的产生，从而客观的避免重复。由于采用了二叉树的结构存放表达式，所以可以再二叉树生成的时候将树根据一点规则判断左右子树的对象 若生成节点的对对象是+或者*
- 左右子树的值不同，则值大的作为左子树
- 左右子树的值相同时，判断子树的运算符优先级大小，优先级大的作为左子树
- 运算符优先级相同，判断子树下的左子树值得大小，值大的作为左子树
- 若为子树为一个为数字，一个为表达式，则表达式作为左子树
- 比较左右树的左子树符号，优先级大的放左边
- 其余情况概率太低，不给予考虑。
 
根据这个规则，基本上包含了交换律可能出现的情况，将可以有交换律变换得到的表达式都转为一个统一的表达式，在根据检查已生成的表达式树的结构，若存在重复的就放弃当前表达式，重新生成并查重。 在这个规则下 3+2+1 与 3+1+2 两个表达式不是重复的表达式 因为不能再有限次的交换律加成为相同的表达式。

但对于添加括号来说左右子树不影响最终运算结果的不添加括号，当前操作若比左子树内部操作优先级高，则加括号，其他情况不添加括号，除当前操作比右子树内部操作优先级低外，右子树不添加括号，其他情况均要求添加括号。使得括号不会相交且比较合适。

	if (operate == 1 or operate == 3) and leftValue <=rightValue :
                # 当右子树值大于左子树时
                if leftValue < rightValue:
                    problemArray = [right['problemArray'], operate, left['problemArray']]
                #     当左右子树值相等时
                else:
                    if (type(left['problemArray']) == list) and (type(right['problemArray']) == list):
                        if left['problemArray'][1] > right['problemArray'][1]:
                            problemArray = [left['problemArray'], operate, right['problemArray']]
                        elif left['problemArray'][1]<right['problemArray'][1]:
                            problemArray = [right['problemArray'], operate, left['problemArray']]
                        else:
                            if left['problemArray'][0] < right['problemArray'][0]:
                                problemArray = [right['problemArray'], operate, left['problemArray']]
                            elif left['problemArray'][0] > right['problemArray'][0]:
                                problemArray = [left['problemArray'], operate, right['problemArray']]
                            else:
                                if left['problemArray'][2] < right['problemArray'][2]:
                                    problemArray = [right['problemArray'], operate, left['problemArray']]
                                    problemArray = [left]
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
　　　　　　

计算表达式结果无论整数分数均转化成为[fenzi,fenmu]形式进行计算，随机产生分数则是利用decchance作为flag来判断是否达到产生分数标准

	def calc(self,operNum1,operNum2,operate):
        '''
        计算值
        :param operNum1: 操作数1
        :param operNum2: 操作数2
        :param operate: 操作
        '''


        if operate == 1:
            fenzi = operNum1[0]*operNum2[1]+operNum2[0]*operNum1[1]
            fenmu = operNum1[1]*operNum2[1]

        elif operate == 2:
            fenzi = operNum1[0]*operNum2[1]-operNum2[0]*operNum1[1]
            fenmu = operNum1[1]*operNum2[1]
            if fenzi < 0:
                return [fenzi, fenmu]
        elif operate == 3:
            fenzi = operNum1[0]*operNum2[0]
            fenmu = operNum1[1]*operNum2[1]

        elif operate == 4:
            fenzi = operNum1[0]*operNum2[1]
            fenmu = operNum1[1]*operNum2[0]

        result = self.stacdardDec(fenzi,fenmu)
        return result
　

接收外部题目文件并对用户答案进行检查的部分主要通过逆波兰表达式计算出标准答案，存放在两个列表（用户和标准答案）中的答案进行比对得到正确与错误题目个数以及题目号

逆波兰表达式的实现过程

&emsp;首先维护两个空栈，（stack_exp）存放逆波兰表达式，(stack_ops)暂存操作符，运算结束后stack_ops必为空

&emsp;&emsp;循环遍历字符串(将表达式分为四种元素 1、数值; 2、操作符; 3、 左括号; 4、右括号)，具体情况如下

&emsp;&emsp;&emsp;1、遇到数值， 将该值入栈stack_exp

&emsp;&emsp;&emsp;2、遇到左括号， 将左括号入栈stack_ops
&emsp;&emsp;&emsp;3、遇到右括号，将stack_ops中的操作符从栈顶依次出栈并入栈stack_exp， 直到第一次遇到左括号终止操作

&emsp;&emsp;&emsp;4、遇到四则运算操作符号（+ - * /）

&emsp;&emsp;&emsp;&emsp;4-1、 如果stack_ops为空， 操作符入栈stack_ops

&emsp;&emsp;&emsp;&emsp;4-2、 如果stack_ops不空，将stack_ops栈顶操作符与遍历到的操作符(op)比较：

&emsp;&emsp;&emsp;&emsp;&emsp;4-2-1： 如果stack_ops栈顶操作符为左括或者op优先级高于栈顶操作符优先级， op入栈stack_ops，当前遍历结束

&emsp;&emsp;&emsp;&emsp;&emsp;4-2-2： 如果op优先级小于或者等于stack_ops栈顶操作符， stack_ops栈顶操作符出栈并入栈stack_exp，重复4-1、 4-2直到op入栈stack_ops

&emsp;&emsp;&emsp;5、字符串遍历结束后如果stack_ops栈不为空，则依次将操作符出栈并入栈stack_exp

	def middle_to_after(s):
    ops_rule = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    expression = []
    ops = []
    ss = s.split(' ')
    for item in ss:
        if item in ['+', '-', '*', '/']:
            while len(ops) >= 0:
                if len(ops) == 0:
                    ops.append(item)
                    break
                op = ops.pop()
                if op == '(' or ops_rule[item] > ops_rule[op]:
                    ops.append(op)
                    ops.append(item)
                    break
                else:
                    expression.append(op)
        elif item == '(':
            ops.append(item)
        elif item == ')':
            while len(ops) > 0:
                op = ops.pop()
                if op == '(':
                    break
                else:
                    expression.append(op)
        else:
            expression.append(item)

    while len(ops) > 0:
        expression.append(ops.pop())

    return expression


	def expression_to_value(expression):
    stack_value = []
    for item in expression:
        if item in ['+', '-', '*', '/']:
            n2 = stack_value.pop()
            n1 = stack_value.pop()
            result = cal(n1, n2, item)
            stack_value.append(result)
        else:
            stack_value.append(int(item))
    return stack_value[0]


	def cal(n1, n2, op):
    if op == '+':
        return n1 + n2
    if op == '-':
        return n1 - n2
    if op == '*':
        return n1 * n2
    if op == '/':
        return n1 / n2
 

#五.测试结果
生成10000道题

![](https://i.imgur.com/jA0JR2l.png)

![](https://i.imgur.com/oalgUxV.png)

对命令行传进文件及答案进行判定  -e exercisefile.txt -a answerfile.txt

![](https://i.imgur.com/J0GxnU2.png)

之前需求没有看清楚需求做出来的功能如下（是在命令行里输入答案，针对生成的题目和用户答案进行检查正误）

![](https://i.imgur.com/QzccO0p.png)


#六.项目小结

结对编程中首先解决的就是工作的合理分配问题，虽然工作做出了分配，，但任务之间的需要的交流与沟通是必不可少的，我知道你要完成的任务是什么，你能给我提供什么，反着来同样如此。最重要的是在做项目的过程中两个人一起解决问题，不论问题是出现在哪一方，我觉得这就是结对编程的结果大于二的原因。