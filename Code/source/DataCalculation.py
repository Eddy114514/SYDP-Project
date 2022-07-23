from scipy.integrate import quad

from Calculation import Calculation


class DataCalculation(Calculation):
    def __init__(self, CDD):
        super().__init__(CDD)
        self.SignData()
        self.Volume_Inside = 0
        self.Volume_Outside = 0
        self.Volume_Styrofoam = 0
        self.Volume_Concrete = 0


    def Canoe_Volume(self):
        # Process of Signing Function
        SwDFunction_List, SwD_Out_Function_List = self.SignFunction_CanoeVolume()
        # Volume
        self.Volume_Inside = self.Inside_Volume(SwDFunction_List)
        self.Volume_Outside = self.Outside_Volume(SwD_Out_Function_List)
        self.Volume_Styrofoam = self.Styrofoam_Volume(SwDFunction_List)
        self.Volume_Concrete = self.Volume_Outside - self.Volume_Inside
        # Uncomment to Debug
        print(self.Volume_Outside, self.Volume_Inside, self.Volume_Concrete)

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
                        print(2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * self.Depth[index])
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
        # if no cover
        if (float(self.CoverLength) == float(0)): return 0

        if (self.Note[2] == 24):
            # minus the B2
            self.Length[1] = self.Length[1] - self.B2
        len_sum = self.GetLengthList(self.Length)[1:]  # don't need 0
        operation_f = self.LocateCover(self.CoverLength, len_sum)
        operation_e = self.LocateCover(len_sum[-1]-self.CoverLength, len_sum)
        Volume_FrontCover = self.Styrofoam_Volume_Calculate(operation_f, SwDFunction_List)
        Volume_EndCover = self.Volume_Inside - self.Styrofoam_Volume_Calculate(operation_e, SwDFunction_List)
        print(Volume_FrontCover,Volume_EndCover)

        return (Volume_EndCover+Volume_FrontCover)

    def Styrofoam_Volume_Calculate(self, op_list, SwDFunction_List):
        volume = 0
        for op in op_list:
            if(op[1] == 0):
                pass # save time
            elif(self.Note[2] != 24):
                # canoe that are not asymmetric
                if (self.WidthFList[op[0]] == -1 and self.DepthFList[op[0]] == -1):
                    volume += op[1] * 2 * \
                              quad(SwDFunction_List[op[0]], 0, self.Depth[op[0]])[0]
                elif (self.WidthFList[op[0]] != -1 and self.DepthFList[op[0]] != -1):
                    volume += 2 * ((self.ECurveF[op[0]]) / (self.ECurveF[op[0]] + 1)) *\
                             quad(SwDFunction_List[op[0]], 0, op[1])[0]
            else:
                if(op[0] == 1):
                    volume += 2 * ((self.ECurveF[op[0]]) / (self.ECurveF[op[0]] + 1)) * self.Depth[op[0]] *\
                              quad(self.WidthFList[op[0]], self.B2, op[1]+self.B2)[0]

                else:
                    volume += 2 * ((self.ECurveF[op[0]]) / (self.ECurveF[op[0]] + 1)) * \
                              quad(SwDFunction_List[op[0]], 0, op[1])[0]
        return volume







    # Helper Function
    @staticmethod
    def LocateCover(canoe_cover, length_list):
        """
        Take coverValue and return list of operation for calculation of volume
        """
        calculation_operation_list = []
        for lenIndex in range(1, len(length_list)):
            if (length_list[lenIndex] >= canoe_cover >= length_list[lenIndex - 1]):
                for index in [lenIndex - 1, lenIndex]:
                    if (canoe_cover >= length_list[index]):
                        calculation_operation_list.append([index, length_list[lenIndex - 1]])
                        canoe_cover = canoe_cover - length_list[lenIndex - 1]
                    else:
                        calculation_operation_list.append([index, canoe_cover])
            elif (canoe_cover < length_list[0] and lenIndex == 0):
                return [0, canoe_cover]  # if the cover is less than the first length

        return calculation_operation_list
