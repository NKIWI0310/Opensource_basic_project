from time import *
from datetime import *

#2019038024 이동민

def countDays(data1, data2):
    retDays = 0
    year, month, day = data1.split('/')
    sDay = date(int(year), int(month), int(day))
    year, month, day = data2.split('/')
    eDay = date(int(year), int(month), int(day))
    diffDays = eDay - sDay
    retDays = diffDays.days
    return retDays


def getDay(t):
    weeks = ['월', '화', '수', '목', '금', '토', '일']
    return weeks[t.tm_wday]


startData, curData, tm = '', '', None

startData = input('시작 날짜(연/월/일) --> ')
tm = localtime()
curData = str(tm.tm_year) + '/' + str(tm.tm_mon) + '/' + str(tm.tm_mday)
print(startData, "부터 오늘(", curData, ")까지는", countDays(startData, curData), "일이 지났습니다")
print("그리고 오늘은", getDay(tm), "요일입니다")
