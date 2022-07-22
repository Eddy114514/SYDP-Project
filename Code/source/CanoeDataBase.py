class CanoeDataBase:
    # Designed to connect to STL database

    def __init__(self, SectionDataDict, HullDataDict):
        self.SDD = SectionDataDict
        self.HDD = HullDataDict
        self.SymmetryBoolean = False

    def ConfigSYM(self):
        print("Change from ", self.SymmetryBoolean)
        # flap the Boolean
        self.SymmetryBoolean = not self.SymmetryBoolean
        print("to", self.SymmetryBoolean)

    def GetSYM(self):
        return(self.SymmetryBoolean)

    def ConstructDict_SDD(self, SectionNum, DataList):
        self.SDD[SectionNum] = DataList

    def ConstructDict_HDD(self, DataList):
        self.HDD = DataList

    def GetData_SDD(self):
        return (self.SDD)

    def GetData_CDD(self):
        return (self.SDD, self.HDD)

    def DeletData_SDD(self):
        del self.SDD

    def DeletData_HDD(self):
        del self.HDD

    def DeletData_CDD(self):
        del self.SDD
        del self.HDD
    def SaveDataToSQL(selfs):
        #Save Data To SQL
        print('work')
    def SaveDataIntoFile(self):
        #Save Data
        print("work")