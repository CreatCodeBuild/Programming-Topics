# map, filter, reduce

def loadData1():
    yield from range(1024 * 1024 * 1024)

def map(f, iterable):
    for x in iterable:
        yield f(x)

def apply(x):
    return x * 10 if x is not None else 10

l = [x for x in map(apply, loadData1())]

'''
produce(?):->iterable
iterator(iterable):->iterable
consumer(iterable):->?
'''
