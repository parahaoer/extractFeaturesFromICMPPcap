list1 = [1, 2, 3]

list2 = [4, 5, 6]

print(list1 + list2)  #  [1, 2, 3, 4, 5, 6] 是一个列表

t = (1, 2, 3)
print(list(t))  # [1, 2, 3] 将元组转换成列表

list3 = [1, 2]
list3.append(3)
list3.append(list2)
print(list3)  # [1, 2, 3, [4, 5, 6]]

list3 += [7]
print(list3)
