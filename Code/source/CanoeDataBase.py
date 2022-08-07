
class CanoeDataBase:
    # Designed to connect to STL database

    def __init__(self, SectionDataDict, HullDataDict):
        self.SDD = SectionDataDict
        self.HDD = HullDataDict
        self.SymmetryBoolean = False
        self.FSDMode = False

    def ConfigSYM(self):
        print("Change from ", self.SymmetryBoolean)
        # flap the Boolean
        self.SymmetryBoolean = not self.SymmetryBoolean
        print("to", self.SymmetryBoolean)

    def ConfigFSD(self):
        print("Change from ", self.FSDMode)
        # flap the Boolean
        self.FSDMode = not self.FSDMode
        print("to", self.FSDMode)


    def GetSYM(self):
        return(self.SymmetryBoolean)

    def GetFSD(self):
        return(self.FSDMode)

    def ConstructDict_SDD(self, SectionNum, DataList):
        self.SDD[SectionNum] = DataList

    def ConstructDict_HDD(self, DataList):
        self.HDD = DataList

    def GetData_SDD(self):
        return (self.SDD)

    def GetData_CDD(self):
        return (self.SDD, self.HDD)

    def DeleteData_SDD(self):
        del self.SDD

    def DeleteData_HDD(self):
        del self.HDD

    def DeleteData_CDD(self):
        del self.SDD
        del self.HDD
    def SaveDataToSQL(self):
        #Save Data To SQL
        print('work')
    def SaveDataIntoFile(self):
        #Save Data
        print("work")
    def SaveStlIntoFile(self,filePath,stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)
    @staticmethod
    def SaveStlIntoFile_static(filePath,stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)




