class Calculation:

    def __init__(self, CanoeDataBase_Object):
        self.SymmetryBoolean = False

        self.CalculationObject = CanoeDataBase_Object
        self.Length = []
        self.Width = []
        self.SemiWidth = []
        self.Depth = []

        self.ECurveF = []
        self.EWidthF = []
        self.EDepthF = []

        self.Density = 0
        self.Thickness = 0
        self.CoverLength = 0
        self.CrewWeight = 0

        self.WidthFList = []
        self.WidthFList_Outside = []
        self.DepthFList = []
        self.DepthFList_Outside = []

        self.B2 = 0
        self.B2_O = 0
        self.B2_Diff = 0

        self.Symmetricity = self.CalculationObject.GetSYM()
        self.FSDMode = self.CalculationObject.GetFSD()

        self.Log = []
        self.LogMenu = {0: "Set Deign -> One Body", 1: "Set Deign -> Two Body", 2: "Set Deign -> Three Body",
                        10: "Set Deign SubProperty -> Symmetric", 11: "Set Deign SubProperty -> Asymmetric",
                        20: "Assign HullType -> Symmetric_Hull", 21: "Assign HullType -> LongShort_Hull",
                        22: "Assign HullType -> Symmetric_Constant Hull",
                        23: "Assign HullType -> Asymmetric_Constant Hull",
                        24: "Assign HullType -> Asymmetric_Hull"}

    def SignData(self):
        SDD, HDL = self.CalculationObject.GetData_CDD()
        # Write Function for generate testprofile
        # with open("SDDHDD",'w') as file: file.write(str([SDD,HDL]))

        for v in SDD.values():
            self.Length.append(v[0])
            self.Width.append(v[1])
            self.SemiWidth.append(v[1] / 2)
            self.Depth.append(v[2])
            self.ECurveF.append(v[3])
            self.EWidthF.append(v[4])
            self.EDepthF.append(v[5])

        self.CoverLength = HDL[0]
        self.Density = HDL[1]
        self.Thickness = HDL[2]
        self.CrewWeight = HDL[3]

        self.Num = len(self.Length)

        self.SignFunction_Main()
        if self.SymmetryBoolean == True:
            self.Log.insert(1, 10)
        elif self.SymmetryBoolean == False:
            self.Log.insert(1, 11)

    def CalDataReturn(self):
        # Print the OperationNote

        for num in self.Log:
            print(self.LogMenu[num])

        self.DataPrint()

    @staticmethod
    def GetLengthList(lengthList):
        # return the list of length with correct x coordinate
        # exp: lengthList[36,120,36]
        # function return [0,36,156,192]
        Sum = 0
        Len_Sum = [0]
        for length in lengthList:
            Sum += length
            Len_Sum.append(Sum)
        return Len_Sum

    def SignFunction_Main(self):

        if (len(self.ECurveF) == 1):
            self.Log.append(0)
            self.SignFunction_SymmetryHull()

        elif (len(self.ECurveF) == 2):
            self.Log.append(1)
            self.SignFunction_TwoBodyHull()

        elif (len(self.ECurveF) == 3):
            self.Log.append(2)
            self.SignFunction_ThreeBodyHull()

    def BuildLambda_Depth(self, index):
        return (lambda x: self.Depth[index] * (x / self.Length[index]) ** self.EDepthF[index])

    def BuildLambda_Depth_O(self, index):

        return (lambda x: (self.Depth[index] + self.Thickness) * (x / (self.Length[index] + self.Thickness)) **
                          self.EDepthF[index])

    def BuildLambda_Depth_O_A(self, index):
        return (
            lambda x: (self.Depth[index] + self.Thickness) * (x / (self.Length[index] + self.B2_Diff)) ** self.EDepthF[
                index])

    def BuildLambda_Depth_Semi(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: self.Depth[0] * (x / SemiLength) ** self.EDepthF[0])

    def BuildLambda_Width(self, index):

        return (lambda x: self.SemiWidth[index] * (x / self.Length[index]) ** self.EWidthF[index])

    # overRidden
    def BuildLambda_Width_A(self, index, length):
        return (lambda x: self.SemiWidth[index] * (x / length) ** self.EWidthF[index])

    def BuildLambda_Width_O(self, index):
        return (lambda x: (self.SemiWidth[index] + self.Thickness) * (x / (self.Length[index] + self.Thickness)) **
                          self.EWidthF[index])

    def BuildLambda_Width_O_A(self, index, length):
        return (lambda x: (self.SemiWidth[index] + self.Thickness) * (x / (length + self.B2_Diff)) **
                          self.EWidthF[index])

    def BuildLambda_Width_Semi(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: self.SemiWidth[0] * (x / SemiLength) ** self.EWidthF[0])

    def BuildLambda_Width_Semi_O(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: (self.SemiWidth[0] + self.Thickness) * (x / (SemiLength + self.Thickness)) ** self.EWidthF[0])

    def BuildLambda_Depth_Semi_O(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: (
                                  self.Depth[0] + self.Thickness) * (x / (SemiLength + self.Thickness)) ** self.EDepthF[
                              0])

    def BuildLambda_Curve_Constant(self, index):

        return (lambda x: (self.Depth[index] * (x / self.SemiWidth[index])
                           ** self.ECurveF[index]))

    def BuildLambda_Curve_Constant_Out(self, index):
        return (lambda x: (self.Depth[index] + self.Thickness) *
                          (x / (self.SemiWidth[index] + self.Thickness))
                          ** self.ECurveF[index])

    def BuildLambda_Curve(self, SemiWidth, Depth, index):

        return (lambda x: (Depth * (x / SemiWidth)
                           ** self.ECurveF[index]))

    def Buldlambda_Curve_Zero(self):
        # build 0 returner
        return (lambda x: 0.0)

    def DataPrint(self):
        print(self.Length)
        print(self.Width)
        print(self.SemiWidth)
        print(self.Depth)

        print(self.ECurveF)
        print(self.EWidthF)
        print(self.EDepthF)

    def SignFunction_SymmetryHull(self):
        self.Log.append(20)

        self.SymmetryBoolean = True

        self.WidthFList.append(self.BuildLambda_Width_Semi()
                               )
        self.WidthFList_Outside.append(self.BuildLambda_Width_Semi_O())
        self.DepthFList.append(self.BuildLambda_Depth_Semi()
                               )
        self.DepthFList_Outside.append(self.BuildLambda_Depth_Semi_O())

    def SignFunction_TwoBodyHull(self):

        if (self.Length[0] == self.Length[1] and self.SemiWidth[0] == self.SemiWidth[1] and self.Depth[0] == self.Depth[
            1] and self.EWidthF[0] == self.EWidthF[1] and self.EDepthF[0] == self.EDepthF[1]):
            self.SymmetryBoolean = True
            self.Log.append(20)
        else:
            self.Log.append(21)

        for index in range(0, len(self.EDepthF)):
            self.WidthFList.append(self.BuildLambda_Width(index))
            self.WidthFList_Outside.append(self.BuildLambda_Width_O(index))
            self.DepthFList.append(self.BuildLambda_Depth(index)
                                   )
            self.DepthFList_Outside.append(self.BuildLambda_Depth_O(index)
                                           )

    def SignFunction_ThreeBodyHull(self):

        if (self.Length[0] == self.Length[2] and self.SemiWidth[0] == self.SemiWidth[2] and self.Depth[0] == self.Depth[
            2] and self.EWidthF[0] == self.EWidthF[2] and self.EDepthF[0] == self.EDepthF[2]):
            self.SymmetryBoolean = True

        if (self.EWidthF[1] == 0 and self.EDepthF[1] == 0):
            self.SignFunction_ThreeBodyHull_Constant(self.SymmetryBoolean)
        elif (self.EWidthF[1] != 0 and self.EDepthF[1] != 0):
            self.SignFunction_ThreeBodyHUll_Asymmetric()

    def SignFunction_ThreeBodyHull_Constant(self, SBoolean):
        if (SBoolean == True):
            self.Log.append(22)
        elif (SBoolean == False):
            self.Log.append(23)

        for index in range(0, len(self.EDepthF)):
            if (self.EWidthF[index] != 0 and self.EDepthF[index] != 0):
                self.WidthFList.append(self.BuildLambda_Width(index))
                self.WidthFList_Outside.append(self.BuildLambda_Width_O(index))
                self.DepthFList.append(self.BuildLambda_Depth(index)
                                       )
                self.DepthFList_Outside.append(self.BuildLambda_Depth_O(index)
                                               )
            elif (self.EWidthF[index] == 0 and self.EDepthF[index] == 0):
                self.WidthFList.append(-1)
                self.WidthFList_Outside.append(-1)
                self.DepthFList.append(-1)
                self.DepthFList_Outside.append(-1)

    def SignFunction_ThreeBodyHUll_Asymmetric(self):
        self.Log.append(24)
        # Confirm Cross-sectional data for Middle Section
        self.Set_FormulaPoint_Asymmetric()

        # Pair Back section base on the Middle
        self.Length[1] = self.Length[1] + self.B2
        self.Width[2] = self.Width[1]
        self.Depth[2] = self.Depth[1]
        self.SemiWidth[2] = self.SemiWidth[1]
        # For remain the consistency of the Data

        # Sign Function for Front

        self.WidthFList.append(
            self.BuildLambda_Width(0))
        self.WidthFList_Outside.append(
            self.BuildLambda_Width_O(0))
        self.DepthFList.append(self.BuildLambda_Depth(0)
                               )
        self.DepthFList_Outside.append(self.BuildLambda_Depth_O(0))

        # Sign Function for Middle

        self.WidthFList.append(
            self.BuildLambda_Width_A(1, self.Length[1]))
        self.WidthFList_Outside.append(
            self.BuildLambda_Width_O_A(1, self.Length[1]))
        self.DepthFList.append(self.Depth[1])
        self.DepthFList_Outside.append((self.Depth[1] + self.Thickness))

        # Sign Function for end

        self.WidthFList.append(
            self.BuildLambda_Width(2))
        self.WidthFList_Outside.append(
            self.BuildLambda_Width_O(2))
        self.DepthFList.append(self.BuildLambda_Depth(2)
                               )
        self.DepthFList_Outside.append(self.BuildLambda_Depth_O(2))

    def Set_FormulaPoint_Asymmetric(self):
        SWvalue = (self.SemiWidth[0]
                   / self.SemiWidth[1]) ** (1 / self.EWidthF[1])
        SWvalue_O = ((self.SemiWidth[0] + self.Thickness)
                     / (self.SemiWidth[1] + self.Thickness)) ** (1 / self.EWidthF[1])

        self.B2 = round((self.Length[1] * SWvalue) / (1 - SWvalue), 10)
        self.B2_O = round(((self.Length[1]) * SWvalue_O) / (1 - SWvalue_O), 10)
        self.B2_Diff = self.B2_O - self.B2

    def Sign_CurveFormula(self, k):
        return (lambda x: (
                self.WidthFList[k](x) * self.DepthFList[k](x)))

    def Sign_CurveFormula_A(self, k):
        return (lambda x: (
                self.WidthFList[k](x) * self.DepthFList[k]))

    def Sign_CurveFormula_Constant(self, k):
        return (lambda x: (((self.SemiWidth[k] ** self.ECurveF[k]) * x) / (self.Depth[k])) ** (1 / self.ECurveF[k]))

    def Sign_CurveFormula_Out(self, k):
        return (lambda x: (
                self.WidthFList_Outside[k](x) * self.DepthFList_Outside[k](x)))

    def Sign_CurveFormula_Out_A(self, k):
        return (lambda x: (
                self.WidthFList_Outside[k](x) * self.DepthFList_Outside[k]))

    def Sign_CurveFormula_Constant_Out(self, k):
        return (lambda x: (
                                  (((self.SemiWidth[k] + self.Thickness) ** self.ECurveF[k]) * x) / (
                                  self.Depth[k] + self.Thickness)) ** (1 / self.ECurveF[k]))
