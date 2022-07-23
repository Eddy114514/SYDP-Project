
lenSum = [0,36,156,192]
cover1 =38
cover2 = 189

def locateCover(cover,list):
    operateList = []
    for lenIndex in range(1,len(list)):
        if(cover <= list[lenIndex] and cover >= list[lenIndex-1]):
            for index in [lenIndex-1,lenIndex]:
                if(cover >= list[index]):
                    operateList.append([index, list[lenIndex-1]])
                    cover = cover - list[lenIndex-1]
                else:
                    operateList.append([index,cover])
        elif(cover < list[0] and lenIndex == 0):
            return [0,cover]
    return operateList
# test demo

print(lenSum[1:])



cover1operateList = locateCover(cover1,[36,156,192])
cover2operateList = locateCover(cover2,lenSum)
print(cover1operateList)
print(cover2operateList)

