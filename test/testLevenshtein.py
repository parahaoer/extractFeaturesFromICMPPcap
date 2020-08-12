def normal_leven(list1, list2):
  len_str1 = len(list1) + 1
  len_str2 = len(list2) + 1
  # 创建矩阵
  matrix = [0 for n in range(len_str1 * len_str2)]
  #矩阵的第一行
  for i in range(len_str1):
    matrix[i] = i
  # 矩阵的第一列
  for j in range(0, len(matrix), len_str1):
    if j % len_str1 == 0:
      matrix[j] = j // len_str1
  # 根据状态转移方程逐步得到编辑距离
  for i in range(1, len_str1):
    for j in range(1, len_str2):
      if list1[i-1] == list2[j-1]:
        cost = 0
      else:
        cost = 1
      matrix[j*len_str1+i] = min(matrix[(j-1)*len_str1+i]+1,
                    matrix[j*len_str1+(i-1)]+1,
                    matrix[(j-1)*len_str1+(i-1)] + cost)
 
  return matrix[-1]

byte_str1 = b'\x08\x00\x0e\xf9,\xe0\x05k\x10\x01"\x0f\x01\x00\x00\x00\x0e\xd6\xac\xa4~\x13\xac\xef\xdc\x01\xe00\xda\xfa\x06'
byte_str2 = b'\x00\x00\x15\xd1,\xe0\x05k\x10\x01"\x0f\x01\x00\x00\x00\x0e\xd6\xac\xa4~\x13\xac\xef\xdc\x01\xe0(\x010\xda\xfa\x06'

list1 = []
list2 = []

for b in byte_str1:
    list1.append(b)

for b in byte_str2:
    list2.append(b)

print(normal_leven(list1, list2)) # ==> 5



