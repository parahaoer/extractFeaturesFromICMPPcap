import multiprocessing


def f(x, arr, l, dict1):
    print(x.value)
    arr[0] = 5
    print('arr[1]=' + str(arr[1]))
    l.append('Hello')
    print(l)
    print(dict1)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    x = manager.Value('d', True)
    arr = manager.Array('i', range(10))
    l = manager.list()
    l.append(["a", "b", "c"])
    dict1 = manager.dict()
    dict1 = {"a": 1, "b": 2}
    x.value = False
    arr[1] = 10
    proc = multiprocessing.Process(target=f, args=(x, arr, l, dict1))
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