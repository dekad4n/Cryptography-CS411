import client as cl
from math import gcd, log

cl.getQ1()

# Q1 SOLUTION

# Q1a
# finding all the elements that has gcd = 1 with 386! (all elements of the group)
cnt = 0
congruence_class = set()
for i in range(1,386):
    if gcd(i, 386) == 1:
        congruence_class.add(i)
        cnt += 1
# cl.checkQ1a(cnt)
# finding a generator, which means a element that has powers which generates group
# we already found the group above
val = None
for currentValue in range(1, 386):
    currentSet = set()
    for everyPower in range(1,386):
        currentSet.add(pow(currentValue, everyPower) % 386)
    if congruence_class == currentSet:
        val = currentValue
        break
print(val)
cl.checkQ1b(val)
# cl.checkQ1c(val)
# cl.checkQ1c(gcd(64,192))
# we are going to find an element that exactly generates 64 elements of the group!
val2 = None
for currentValue in range(1, 386):
    currentSet = set()
    for everyPower in range(1, 386):
        currentSet.add(pow(currentValue, everyPower) % 386)
    if len(currentSet) == 64:
        val2 = currentValue
        break
print(val2)
# cl.checkQ1c(val2)
