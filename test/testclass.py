class testA():
    print("在class内代码执行")
    varA = '我是全局变量？'

    def func(self):
        print(self.varA)


# testA = testA()
# testA.func()


class testB(testA):
    def funcB(self):
        super().func()
        self.func()


testB = testB()
testB.funcB()
