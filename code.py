'''
Performance
1. Data Structure
    a. Proper Data Structure                                         合适的数据结构
    b. Proper Initialization/Construction/Allocation Method          合适的构造方法

2. Algorithm
    a. Proper Initialization/Construction/Allocation of Your 1.a  
    b. Proper interaction with 1.a                                   恰当的数据结构使用

3. Design
    a. Concurrent vs. Not Concurrent
    b. Parallel   vs. Serial
'''

def loadData1(): # 6 s
    return [None] * (1024 * 1024 * 1024)

def loadData2(): # 63 s
    return [None for i in range(1024 * 1024 * 1024)]

def loadData3(): # 90 s
    l = [] # dynamic array, array list
    for i in range(1024 * 1024 *1024):
        l.append(None)
    return l

from collections import deque  # linked list
def loadData4(): # 57 s
    l = deque()
    for i in range(1024 * 1024 *1024):
        l.append(None)
    return l

def loadData5(): # 47 s
    return deque(None for i in range(1024 * 1024 * 1024))

# [] is dynamic array, ~=ArrayList (Java), ~=Go (Slice)


# from time import time
# s = time()

# loadData5()

# t = time() - s
# print(t)
