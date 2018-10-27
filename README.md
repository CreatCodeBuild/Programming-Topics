# Programming-Topics
Common Programming Topics and My Thoughts on Them

I've been thinking about common topics or say common category of problems in programming a lot recently because I believe understanding problems is the most important part of mastering the art of programming. Many tutorials or say educational materials focus on solutions instead of problems.

For example, how to do X in language Y without really pointing out the fundamental problem X is trying to address such that the knowledge gained can be easily transfered to how to do X_version_2 in language Z.

# Structural Mismatch
One of such problems is __Structural Mismatch__. I am not sure if this is the academic word for this problem but this is the word I heard from Rob Pike, the creator of Go programming language, in one of his talk: [Lexical Scanning in Go](https://www.youtube.com/watch?v=HxaD_trXwRE)

I probably watched this talk in end of 2017 and I watched this talk several times more in 2018. And I kept thinking:
### Is tokenizer too big an example to explain this problem to new or intermediate programmers?
I call a tokenizer "too big" because if a person is new to programming, I don't think she will write a parser for a compiler. Even professional programmer like me have never written a parser before. I really want to expand this talk with simpler and day to day work related exmaples and tell the essential ideas about __Structural Mismatch__ porblem.

## What is it?
Any programmer must have seen it, with or without the recognition. Let's say we have a hash map of name to age.
```
{
  "John": 17
  "Adam": 19
  "Mike": 18
}
```
A programmer wants to convert it to a list of tuples.
```
[
  ("John", 17)
  ("Adam", 19)
  ("Mike", 18)
]
```
Let's use Python as an example
```python
def DictToList(d):  # not pep8, who cares?
  l = [None] * len(d)
  for i, e in enumerate(d.items()):
    l[i] = e
```
You have just witnessed a structural mismatch problem and its solution!

__A structural mismatch problem is where you have a data type and you want to translate it to another type while preserve all the information you care about, no more, no less.__

The mismatch is created by the structural difference of 2 types. In this example, we have a list of tuple vs. a hash map.

### What could be a problem of this implementation?
What if the input has unknown amount of data?
```python
def DictToList(d):  # not pep8, who cares?
  l = []
  for e in d.items():
    l.append(e)
```
This solves the problem except that it's slow if the length of `d` is large.

The built-in Python `list` is dynamic array which is not ideal for large amount of appending. Here I use Python as an example, but the take away is about __choosing proper data structures__.

For example, an efficient queue implementation might be a good choice.
```python
import collections
def DictToList(d):
  l = collections.deque()
  for e in d.items():
    l.append(e)
```

### Different Target Types
Let's refresh our definiton of structural mismatch again: Translating a sequence of type X to a nother sequence of type Y.
Simply denote it as:
`S[X] -> T[Y]`

The above example can be written as `Dict[key value pair] -> List[Tuple]`.

What if your PM tells you that we don't want tuples anymore? What if we now needs
```python
class MyType:
  def __init__(self, x, y):
    self.x = x
    self.y = y
```
The problem of our last implementaion is that we coupled the iteration of items with the translation of the itmes. We can decouple them as
```
def DictToX(d, trans):
  l = collections.deque()
  for e in d.items():
    l.append(trans(e))
```
where `trans(element in dict) -> any type`

We can then define our own transItemToMyType:
```
def DictToMyTypeList(d):
  def trans(e):
    return MyType(e[0], e[1])

  return DictToX(d, trans)
```

__"Wait, did you just reinvented `map` func? This article is wasting my time!"__

Yes, `map` func in Python, particularly the generator map in Python3 is strongly related to the topic of this article. The idea of `map` is that as long as the source container and the targeting container are iterable, namly sequences, you can apply any kind of transformation to the contained elements. `map` does the iteration and assumes nothing more. It is a generic `S[X] -> T[Y]` solution.

More importantly, let's think about the big question of why Python3 changed `map`'s returned type from a `list` to a `generator`?

To answer this question, we need to ask ourself 3 more questions about `S[X] -> T[Y]`:
1. What if the size of `S` is very big?
2. What if the size of `S` is infinite?
3. What if the consumer of `T[Y]` doesn't care about all `Y`s in their totality?
4. What if you do not even have `S[X]` in its totality?

### What if the size of `S` is very big?
If the size of `S[X]` is `65GB` which is larger than half of your memory, say `128GB`, you can't hold `T[Y]` in memory at once because `T[Y]`'s size is likely to be similar to `S[X]`

### What if the size of `S` is infite?
This is related to No.4

### What if the consumer of `T[Y]` doesn't care about all `Y`s in their totality?
Let's say your are writing a server which receives file uploads. `S[X]` represents the complete file a user is uploading. `S` represents a file format and `X` represents a chunk of this file. `T[Y]` represents the complete file your server needs to write to the persistent storage. Your server accepts multiple upload formats but you decode all of them to a single format `T`, that's why you have this `S vs T` problem. Of course `Y` represents a chunk of `T`.

It would be stupid to hold all received data in memory before `S[X]` is complete and then starts the trans-coding and writing. You would want to start trans-coding and writing as long as enough data has been received to make the decision, for exmaple, once the format meta data is received.

### What if you do not even have `S[X]` in its totality?
Take the example in No.3, you won't have `S[X]` in total at first, but you will eventually. What if your `S[X]` is in the client and represents a data visualization of stock prices? It is the real time data streamed from a server. You will never have all of `S[X]`.

More strangely, your client may not even needs to store all of the historical data, it probaly only wants to display to real time current data.

__This is where the concurrent design part kicks in__

## Concurrent Design and Structural Mismatch
