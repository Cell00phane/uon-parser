tel = {'jack': 4098, 'sape': 4139}
print(tel["jack"])

data = [('key', ['item0', 'item1', 3.14])]

d = dict(data)

tup = ('Jackie', 4000)
tup2 = ('Jacko', 4400)
d2 = dict([tup, tup2])
print(d2)

l = [1,2, None]

class A:
    def __init__(self, otherObject):
        otherObject.doSomething()
        self.otherObject = otherObject

    def doSomething(self):
        print("do Something in A")

class B:
    def doSomething(self):
        print("do Something in B")

class C:
    def doSomething(self):
        print("do Something in C")


b = B()
c = C()
a = A(c)