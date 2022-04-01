import random
def getNumber(strData):
    numStr = ''
    for ch in strData:
        if ch.isdigit():
            numStr +=ch

    return int(numStr)

#2019038024 이동민

data = []
i,k = 0,0

for i in range(0,10):
    tmp = hex(random.randrange(0,100000))
    tmp = tmp[2:]
    data.append(tmp)

print("정렬 전 데이터 : ",end = ' ')
for num in data:
    print(num,end=' ')

for i in range(0, len(data)-1):
    for k in range(i+1,len(data)):
        if getNumber(data[i]) > getNumber(data[k]):
            tmp = data[i]
            data[i] = data[k]
            data[k] = tmp

print("\n정렬 후 데이터 : ",end = ' ')
for num in data:
    print(num,end=' ')