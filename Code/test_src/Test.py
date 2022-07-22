class A:
    def __init__(self,x):
        self.num = x

class B(A):
    def __init__(self,x):
        super().__init__(x)

    def returnNum(self):
        return self.num

A(1)
A.returnNum()