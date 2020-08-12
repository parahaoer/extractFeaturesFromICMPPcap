a = 4

def testfun():
    global a 
    print(a) # ==> 在函数中可以直接调用全局变量

def testfun2():
    global a 
    a = 6
    testfun()

if __name__ == "__main__":
    testfun2()
