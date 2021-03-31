def a():
    return 10

# print(5//2)

# a= {1:2,2:2}
# print(a.items())

# try:
#     [1,2][4]
#     except IndexError:
#         print("Loon")

# a = {1:9,2:8,3:7,4:6,5:5}
# print(a.get(6))

# def f():
#     f()
#     return 42
# f()

# print("hello"'world'*2)

import re

m = re.search(r'(ab[cd]?)',""""acdeabdabcde"""")
print(m.groups())