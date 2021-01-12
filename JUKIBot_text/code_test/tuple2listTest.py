from collections import deque

l = ["aaa","bbb","ccc"]
t = tuple(l)
print(l)
print(t)
print(bool(t == ("aaa","bbb","ccc")))

queue = deque([1,2,3,4,5],maxlen=5)
print(type(queue))
print(list(queue))

print(list(range(4,0,-1)))