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

The built-in Python `list` is dynamic array which is not ideal for large amount of appending. Here I use Python as an example, but the take away is about choosing proper data structures.
