import random
data = []
i,k =0,0

for i in range(0,10):
    temp = hex(random.randrange(0,1000))
    data.append(temp)

print("정렬전 데이터 : ", end = '')
for i in range(0,10):
    print(data[i] , " " , end = '')

for i in range(0,len(data)-1):
    for k in range(i+1,len(data)):
        if int(data[i],16) > int(data[k],16):
            temp = data[i]
            data[i] = data[k]
            data[k] = temp

print("\n 정렬 후 데이터 : ", end = '')
for i in range(0,10):
    print(data[i] , " " , end = '')
