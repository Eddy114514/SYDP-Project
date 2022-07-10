from CanoeDataBase import CanoeDataBase
from Calculation import Calculation
import sys

class DebugBase():
    def __init__(self, profile):
        self.profile = profile

    def Debug(self, p):
        FileName = "TestProfile_" + p + ".txt"
        with open(f'..\\..\\asset\\TestProfile\\{FileName}') as List:
            read = List.read()
            Data = eval(read)

        SectionDictObject = Data[0]
        HullDictObject = Data[1]
        self.CDD = CanoeDataBase(SectionDictObject, HullDictObject)
        self.CCO = Calculation(self.CDD)

        # Test
        self.CCO.CalDataReturn()
        self.CCO.Canoe_Volume()
        # End the Program
        End = input("Enter 'space' to end the Program")
        if(End == ' '):
            sys.exit()



class HealthCheckBase():
    # TBD
    def __init__(self, ClassType):
        self.CT = ClassType

    def ErrorReturn(self, string):
        # return warning & error when wrong data input
        return 42

    def HCheck(self):
        # check the ability of program to run
        return 42
