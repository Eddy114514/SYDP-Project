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

        self.Buoyancy = 0
        self.Buoyancy_Submerge = 0

        self.CanoeWeight = 0
        self.TotalWeight = 0

        self.SubmergeBoolean = False
        self.FlowBoolean = False


    def CalDataReturn(self):
        # Print the OperationNote
        # Not Done Yet
        OperationNote = []
        for num in self.Note:
            print(self.NoteMenu[num])
            OperationNote.append(self.NoteMenu[num])
        self.DataPrint()

        return OperationNote

    def DataPrint(self):
        print(f"Length: {self.Length}")
        print(f"Width: {self.Width}")
        print(f"SemiWidth: {self.SemiWidth}")
        print(f"Depth: {self.Depth}")
        print("\n")
        print(f"Function of Exponent of Curve{self.ECurveF}")
        print(f"Function of Exponent of Width{self.EWidthF}")
        print(f"Function of Exponent of Depth{self.EDepthF}")
        print("\n")
        print(f"Inside Volume: {self.Volume_Inside}")
        print(f"Volume_Outside: {self.Volume_Outside}")
        print(f"Volume_Styrofoam: {self.Volume_Styrofoam}")
        print(f"Volume_Concrete: {self.Volume_Concrete}")
        print("\n")
        print(f"CanoeWeight = {self.CanoeWeight}")
        print(f"TotalWeight = {self.TotalWeight}")
        print(f"Buoyancy = {self.Buoyancy}")
        print(f"Buoyancy_Submerge = {self.Buoyancy_Submerge}")
        print("\n")
        print(f"SubmergeBoolean = {self.SubmergeBoolean}")
        print(f"FlowBoolean = {self.FlowBoolean}")

    def CanoeDataCalculation(self):
        self.Canoe_Volume()
        self.Canoe_Weight()
        self.Canoe_Buoyancy()
        self.Canoe_Flowability()

    def Canoe_Weight(self):
        # inch_to_feet = 1728 || inch³ ==> feet³
        self.CanoeWeight = (self.Volume_Concrete/1728)*self.Density
        self.TotalWeight = self.CanoeWeight + self.CrewWeight

    def Canoe_Buoyancy(self):
        # inch_to_meter = 61023.744095 || inch³ ==> m³
        # gravity = 9.8 || Earth
        # density_Water =  997 kg/m³
        # Buoyancy (N) = ρgV = 997*9.8*(Volume/61023.744095) = Volume * 0.160111447518  || The displacement of water
        self.Buoyancy = self.Volume_Outside * 0.160111447518
        self.Buoyancy_Submerge = (self.Volume_Concrete+self.Volume_Styrofoam)*0.160111447518

    def Canoe_Flowability(self):
        # kg_to_lbs = 2.205 || kilogram ==> pound mass
        # F = mg ==> m = f/g
        # (f/g) = kg, kg/2.205 = lbs ==> (f/9.8)/2.205 = 0.225
        capability = self.Buoyancy * 0.225
        capability_submerge = self.Buoyancy_Submerge * 0.225
        if(capability > (self.TotalWeight)):
            self.FlowBoolean = True
        if(capability_submerge > self.CanoeWeight):
            self.SubmergeBoolean = True

    def Canoe_Volume(self):
        # Process of Signing Function
        SwDFunction_List, SwD_Out_Function_List = self.SignFunction_CanoeVolume()
        # Volume
        self.Volume_Inside = self.Inside_Volume(SwDFunction_List)
        self.Volume_Outside = self.Outside_Volume(SwD_Out_Function_List)
        self.Volume_Styrofoam = self.Styrofoam_Volume(SwDFunction_List)
        self.Volume_Concrete = self.Volume_Outside - self.Volume_Inside
        # Uncomment to Debug
        #print(self.Volume_Outside, self.Volume_Inside, self.Volume_Concrete)

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
        # if no cover
        if (float(self.CoverLength) == float(0)): return 0

        if (self.Note[2] == 24):
            # minus the B2
            self.Length[1] = self.Length[1] - self.B2
        len_sum = self.GetLengthList(self.Length)[1:]  # don't need 0
        if(len(len_sum)== 1):
            # symmetric hall
            len_sum = [len_sum[0]/2,len_sum[0]]
            operation_f =self.LocateCover(self.CoverLength, len_sum)
            # avoid Out Erro
            operation_e = operation_f + []
            operation_e[0][1] = self.CoverLength # can be configured
            Volume_FrontCover = self.Styrofoam_Volume_Calculate(operation_f, SwDFunction_List)
            Volume_EndCover = self.Styrofoam_Volume_Calculate(operation_e, SwDFunction_List)
        else:
            operation_f = self.LocateCover(self.CoverLength, len_sum)
            operation_e = self.LocateCover(len_sum[-1] - self.CoverLength, len_sum)
            Volume_FrontCover = self.Styrofoam_Volume_Calculate(operation_f, SwDFunction_List)
            Volume_EndCover = self.Volume_Inside - self.Styrofoam_Volume_Calculate(operation_e, SwDFunction_List)

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
            elif (canoe_cover < length_list[0] and lenIndex-1 == 0):
                return [[0, canoe_cover]]  # if the cover is less than the first length

        return calculation_operation_list
