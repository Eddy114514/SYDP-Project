from CanoeDataBase import CanoeDataBase
from Calculation import Calculation


class DebugBase():
    def __init__(self, profile):
        self.profile = profile

    def Debug(self, p):
        FileName = "TestProfile_" + p + ".txt"
        with open(f'..\\asset\\{FileName}') as List:
            Data = eval(List.read())

        SectionDictObject = List[0]
        HullDictObject = List[1]
        self.CDD = CanoeDataBase(SectionDictObject, HullDictObject)
        self.CCO = Calculation(self.CCO)

        # Test
        self.CCO.Model_Generate()


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
