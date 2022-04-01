inStr, outStr = "", ""
ch = ""
cnt,i = 0,0

#2019038024 이동민

inStr = input("문자열을 입력하세요 : ")
cnt = len(inStr)

for i in range (0,cnt):
    ch = inStr[i]
    if(ord(ch) >= ord("A") and ord(ch) <= ord("Z")):
        newCh = ch.lower()
    elif(ord(ch) >= ord("a") and ord(ch) <= ord("z")):
        newCh = ch.upper()

    outStr += newCh

print("대소문자 변호나결과 --> {0}".format(outStr))