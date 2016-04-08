import re

def transfer_idcard_to18(idcard):
    validCardPattern = re.compile(r'^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$')
        if not validCardPattern.match(idcard) :
            print "please input valid idcard number(15)"
                return ""

        #insert year 19XX
        idcard18 = idcard[0:6] + "19" + idcard[6:]

        idCardWi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        idCardY = [1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        idCardWiSum = 0

        #compute the last char
        for i in range(17):
            idCardWiSum += int(idcard18[i:i+1]) * idCardWi[i]

        idCardMod = idCardWiSum % 11;

        #append last char
        if idCardMod == 2:
            idcard18 = idcard18 + "X"
        else:
            idcard18 = idcard18 + str(idCardY[idCardMod])

        return idcard18

#//for test
if __name__ == "__main__":
    print transfer_idcard_to18("370802940221002")
