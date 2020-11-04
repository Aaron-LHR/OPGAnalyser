import sys
from collections import deque

lines = ["i+i*i*\r\n", "i+i\r\n", "i+\r\n", "ii\r\n"]

with open(sys.argv[1], mode='r', encoding='utf-8') as file:
    lines = file.readlines()
    # print(lines)

operator = {'+': 0, '*': 1, '(': 2, ')': 3, 'i': 4, '#': 5}

matrix = [[0 for i in range(6)] for j in range(6)]
matrix[operator['+']][operator['+']] = 1  # >
matrix[operator['+']][operator['*']] = 2  # <
matrix[operator['+']][operator['(']] = 2  # <
matrix[operator['+']][operator[')']] = 1  # >
matrix[operator['+']][operator['i']] = 2  # <
matrix[operator['+']][operator['#']] = 1  # >

matrix[operator['*']][operator['+']] = 1  # >
matrix[operator['*']][operator['*']] = 1  # >
matrix[operator['*']][operator['(']] = 2  # <
matrix[operator['*']][operator[')']] = 1  # >
matrix[operator['*']][operator['i']] = 2  # <
matrix[operator['*']][operator['#']] = 1  # >

matrix[operator['(']][operator['+']] = 2  # <
matrix[operator['(']][operator['*']] = 2  # <
matrix[operator['(']][operator['(']] = 2  # <
matrix[operator['(']][operator[')']] = 3  # =
matrix[operator['(']][operator['i']] = 2  # <

matrix[operator[')']][operator['+']] = 1  # >
matrix[operator[')']][operator['*']] = 1  # >
matrix[operator[')']][operator[')']] = 1  # >
matrix[operator[')']][operator['#']] = 1  # >

matrix[operator['i']][operator['+']] = 1  # >
matrix[operator['i']][operator['*']] = 1  # >
matrix[operator['i']][operator[')']] = 1  # >
matrix[operator['i']][operator['#']] = 1  # >

matrix[operator['#']][operator['+']] = 2  # <
matrix[operator['#']][operator['*']] = 2  # <
matrix[operator['#']][operator['(']] = 2  # <
matrix[operator['#']][operator[')']] = 2  # <
matrix[operator['#']][operator['i']] = 2  # <

for line in lines:
    stack = []
    line = '#' + line[:-1] + '#'
    i = 1
    stack.append('#')
    while i < len(line):
        ch = line[i]
        j = len(stack) - 1
        while j >= 0:
            if stack[j] != 'N':
                if matrix[operator[stack[j]]][operator[ch]] == 2 or matrix[operator[stack[j]]][operator[ch]] == 3:  # 移进
                    stack.append(ch)
                    print("I" + ch)
                    i += 1
                    break
                elif matrix[operator[stack[j]]][operator[ch]] == 1:  # 规约
                    cur = stack[j]
                    j -= 1
                    while j >= 0:
                        if stack[j] != 'N':
                            if matrix[operator[stack[j]]][operator[cur]] == 2:
                                k = j + 1
                                flag = False
                                while k < len(stack):
                                    if stack[k] == "+" or stack[k] == "*":
                                        if stack[k - 1] != "N" or k + 1 >= len(stack) or stack[k + 1] != "N":
                                            print("RE")
                                            i = len(line)
                                            flag = True
                                            break
                                    k += 1
                                if flag:
                                    break
                                for k in range(len(stack) - 1 - j):
                                    stack.pop()
                                stack.append("N")
                                print("R")
                                break
                            elif matrix[operator[stack[j]]][operator[cur]] == 3:
                                cur = stack[j]
                        j -= 1
                    break
                elif ch == '#' and len(stack) == 2 and stack[0] == '#' and stack[1] == 'N':
                    i = len(line)
                    break
                elif matrix[operator[stack[j]]][operator[ch]] == 0:  # 不存在相邻关系
                    print("E")
                    i = len(line)
                    break
            else:
                j -= 1
