from Calculation import Calculation
from scipy.integrate import quad


class DataCalculation(Calculation):
    def __init__(self, CDD):
        super().__init__(CDD)
        self.SignData()

    def Canoe_Volume(self):
        # Process of Signing Function
        SwDFunction_List, SwD_Out_Function_List = self.SignFunction_CanoeVolume()
        # Volume
        Volume_Inside = self.Inside_Volume(SwDFunction_List)
        Volume_Outside = self.Outside_Volume(SwD_Out_Function_List)
        Volume_Styrofoam = self.Styrofoam_Volume(SwDFunction_List)
        Volume_Concrete = Volume_Outside - Volume_Inside
        # Uncomment to Debug
        print(Volume_Outside, Volume_Inside, Volume_Concrete)

    def SignFunction_CanoeVolume(self):
        SwDFunction_List = []
        SwD_Out_Function_List = []
        if (self.Note[2] != 24):  # Check if it is Asymmetric hall
            for k in range(0, len(self.WidthFList)):
                if (self.WidthFList[k] == -1 and self.DepthFList[k] == -1 and self.WidthFList_Outside[k] == -1 and
                        self.DepthFList_Outside[k] == -1):
                    SwDFunction_List.append(self.Sign_CurveFormula_Constant(k))
                    SwD_Out_Function_List.append(
                        self.Sign_CurveFormula_Constant_Out(k))

                elif (self.WidthFList[k] != -1 and self.DepthFList[k] != -1 and self.WidthFList_Outside[k] != -1 and
                      self.DepthFList_Outside[k] != -1):
                    SwDFunction_List.append(self.Sign_CurveFormula(k))
                    SwD_Out_Function_List.append(self.Sign_CurveFormula_Out(k))

        elif (self.Note[2] == 24):  # Asymmetric hall

            for k in range(0, len(self.WidthFList)):
                if (k == 1):
                    SwDFunction_List.append(self.Sign_CurveFormula_A(k))
                    SwD_Out_Function_List.append(
                        self.Sign_CurveFormula_Out_A(k))
                else:
                    SwDFunction_List.append(self.Sign_CurveFormula(k))
                    SwD_Out_Function_List.append(
                        self.Sign_CurveFormula_Out(k))

        return (SwDFunction_List, SwD_Out_Function_List)

    def Outside_Volume(self, SwD_Out_Function_List):
        Volume_Outside_List = []
        if (len(self.WidthFList) == 1 and len(self.DepthFList) == 1):
            Volume_Outside_List.append(2 * 2
                                       * ((self.ECurveF[0]) / (self.ECurveF[0] + 1))
                                       * quad(SwD_Out_Function_List[0], 0, self.Length[0] / 2 + self.Thickness)[0])

        elif (len(self.WidthFList) != 1 and len(self.DepthFList) != 1):
            if (self.Note[2] != 24):  # Check if it is Asymmetric hall
                for index in range(0, len(self.WidthFList)):
                    if (self.WidthFList[index] == -1 and self.DepthFList[index] == -1):
                        Volume_Outside_List.append(
                            self.Length[index] * 2 *
                            quad(SwD_Out_Function_List[index], 0, (self.Depth[index] + self.Thickness))[0])
                    elif (self.WidthFList[index] != -1 and self.DepthFList[index] != -1):
                        Volume_Outside_List.append(2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * quad(
                            SwD_Out_Function_List[index], 0, self.Length[index] + self.Thickness)[0])
            else:
                # Asymmetric hall
                for index in range(0, len(self.WidthFList)):
                    if (index == 1):
                        Volume_Outside_List.append(
                            2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) *
                            (self.Depth[index] + self.Thickness) *
                            quad(self.WidthFList_Outside[index], self.B2_O, self.Length[index] + self.B2_Diff)[0])
                    else:
                        Volume_Outside_List.append(2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * quad(
                            SwD_Out_Function_List[index], 0, self.Length[index] + self.Thickness)[0])
        # Uncomment to Debug
        return sum(Volume_Outside_List)

    def Inside_Volume(self, SwDFunction_List):
        Volume_Inside_List = []
        if (len(self.WidthFList) == 1 and len(self.DepthFList) == 1):

            Volume_Inside_List.append(2 * 2
                                      * ((self.ECurveF[0]) / (self.ECurveF[0] + 1))
                                      * quad(SwDFunction_List[0], 0, self.Length[0] / 2)[0])


        elif (len(self.WidthFList) != 1 and len(self.DepthFList) != 1):
            if (self.Note[2] != 24):  # Check if it is Asymmetric hall
                for index in range(0, len(self.WidthFList)):
                    if (self.WidthFList[index] == -1 and self.DepthFList[index] == -1):
                        Volume_Inside_List.append(
                            self.Length[index] * 2 * quad(SwDFunction_List[index], 0, self.Depth[index])[0])
                    elif (self.WidthFList[index] != -1 and self.DepthFList[index] != -1):
                        Volume_Inside_List.append(
                            2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) *
                            quad(SwDFunction_List[index], 0, self.Length[index])[0])
            else:
                # Asymmetric hall
                for index in range(0, len(self.WidthFList)):
                    if (index == 1):
                        Volume_Inside_List.append(
                            2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * self.Depth[index] *
                            quad(self.WidthFList[index], self.B2, self.Length[index])[0])
                    else:
                        Volume_Inside_List.append(
                            2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) *
                            quad(SwDFunction_List[index], 0, self.Length[index])[0])
        # Uncomment to Debug
        [print(f"Inside Volume = {volume}") for volume in Volume_Inside_List]

        return sum(Volume_Inside_List)

    def Styrofoam_Volume(self, SwDFunction_List):
        lengthList = self.Length
        if (self.Note[2] == 24):
            # minus the B2
            self.Length[1] = self.Length[1] - self.B2
        # lengthList.append()
        # TBD
        # steps:
        # get a list of length, find where cover is. Calculate
        return 42
