import multiprocessing

def f(x, arr, l):
    print(x.value)
    arr[0] = 5
    l.append('Hello')

if __name__ == '__main__':
        manager = multiprocessing.Manager() 
        x    = manager.Value('d', True)
        arr  = manager.Array('i', range(10))
        l    = manager.list()
        x.value = False
        proc = multiprocessing.Process(target=f, args=(x, arr, l))
        proc.start()
        proc.join()

        print(x.value)
        print(arr)
        print(l)


# from multiprocessing import Process, Manager

# def f(d, l):
#     d[1] = '1'
#     d['2'] = 2
#     d[0.25] = None
#     l.reverse()

# if __name__ == '__main__':
#     with Manager() as manager:
#         d = manager.dict()
#         l = manager.list(range(10))

#         p = Process(target=f, args=(d, l))
#         p.start()
#         p.join()

#         print(d)
#         print(l)