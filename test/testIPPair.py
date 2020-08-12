
def getIPPair(dict1, ip1, ip2, val):

    key1 = (ip1, ip2)
    key2 = (ip2, ip1)

    if key1 and key2 not in dict1.keys():
        dict1[key1] = []

    if key1 in dict1.keys():
        dict1[key1].append(val)
    elif key2 in dict1.keys():
        dict1[key2].append(val)


dict1 = {}

getIPPair(dict1, 1,2,3)
getIPPair(dict1, 2,1,4)

print(dict1)


