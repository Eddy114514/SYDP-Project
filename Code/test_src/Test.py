list = []
list2 = []
def buildlambda(i):
    return lambda x:x+i
for i in range(2):
    # append lambda x:x+0
    # append lambda x:x+1
    list.append(lambda x:x+i)
    list2.append(buildlambda(i))



print("dont use build")
print(list[0](1),list[0])
print(list[1](1),list[1])
print("use build")
print(list2[0](1),list[0])
print(list2[1](1),list[1])