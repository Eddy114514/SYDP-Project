import numpy as np

from Calculation import Calculation


class OptimizationCalculation(Calculation):
    def __init__(self, CDD, CDDRange):
        # DataStructure of CDDRange:
        """
        :type CDDRange: dict{"Section":int,"Interval":float,"ECurveF":[lower,upper],
        ""Exponent of Width"":{sectionNum:[lower,upper]...},""Exponent of Depth"":{sectionNum:[lower,upper]}, }
        """
        super().__init__(CDD)
        self.SignData()
        self.CDDRange = CDDRange

        self.OptimizationPrepare()
        self.SectionDict = {}

        self.Top3 = []
        self.ResultLog = []

    def OptimizationPrepare(self):
        # Locate Cover
        if (self.Log[2] == 24):
            self.Length[1] = self.Length[1] - self.B2
        len_sum = self.GetLengthList(self.Length)[1:]  # don't need 0

        if (len(len_sum) == 1):
            # symmetric hall
            len_sum = [len_sum[0] / 2, len_sum[0]]
            self.operation_f = self.LocateCover(self.CoverLength, len_sum)
            # avoid Out Erro
            self.operation_e = self.operation_f + []
            self.operation_e[0][1] = self.CoverLength  # can be configured
        else:
            self.operation_f = self.LocateCover(self.CoverLength, len_sum)
            self.operation_e = self.LocateCover(len_sum[-1] - self.CoverLength, len_sum)

        if (self.Log[2] == 24):
            self.Length[1] = self.Length[1] + self.B2

    def Optimization(self):
        for ECurveF in np.arange(self.CDDRange["ECurveF"][0], self.CDDRange["ECurveF"][1], self.CDDRange["Interval"]):
            for section in range(self.CDDRange["Section"]):
                if (section in self.SectionDict):
                    self.GenerateSection(ECurveF, section)
                else:
                    self.SectionDict[section] = []
                    self.GenerateSection(ECurveF, section)

        # Start Selection
        if (len(self.SectionDict) == 1):
            self.Optimization_Onebody()
        elif (len(self.SectionDict) == 2):
            self.Optimzation_TwoBody()
        elif (len(self.SectionDict) == 3):
            self.Optimzation_Threebody()

        print(self.Top3)
        return self.Top3, self.ResultLog

    def Optimization_Onebody(self):
        for Combaination in self.SectionDict[0]:
            ECF = Combaination[0]
            EWF = Combaination[1]
            EDF = Combaination[2]
            # Get Basic Data

            InsideVolume = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[0], self.SemiWidth[0], self.Length[0] / 2,
                ECF, EWF, EDF,
                                                  self.Length[0] / 2, 0) * 2

            OutsideVolume = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[0] + self.Thickness, self.SemiWidth[0] + self.Thickness,
                (self.Length[0] / 2) + self.Thickness,
                ECF, EWF, EDF,
                (self.Length[0] / 2) + self.Thickness, 0) * 2

            ConcreteVolume = OutsideVolume - InsideVolume
            CanoeWeight = (ConcreteVolume / 1728) * self.Density
            TotalWeight = CanoeWeight + self.CrewWeight
            Capability = OutsideVolume * 0.160111447518 * 0.225

            if (TotalWeight < Capability):
                # Second Round
                StryofoamVolume = self.Styrofoam_Volume_Calculate(self.operation_f, [ECF], [EWF], [EDF]) + \
                                  self.Styrofoam_Volume_Calculate(self.operation_e, [ECF], [EWF], [EDF])
                submerge = (StryofoamVolume + ConcreteVolume) * 0.160111447518 * 0.225
                if (submerge > CanoeWeight):
                    # Can be take into account
                    self.ResultLog.append([CanoeWeight, ([ECF], [EWF], [EDF])])
        self.ResultLog.sort(key=lambda x: x[0])
        self.Top3 = self.ResultLog[0: 3]

        self.ResultLog = len(self.ResultLog)

    def Optimzation_TwoBody(self):
        FrontList = []
        # Get Basic Data
        for Combaination in self.SectionDict[0]:
            ECF1 = Combaination[0]
            EWF1 = Combaination[1]
            EDF1 = Combaination[2]

            Front = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[0], self.SemiWidth[0],
                (self.Length[0]),
                ECF1, EWF1, EDF1,
                self.Length[0], 0)
            Front_Out = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[0] + self.Thickness, self.SemiWidth[0] + self.Thickness,
                (self.Length[0] + self.Thickness),
                ECF1, EWF1, EDF1,
                self.Length[0] + self.Thickness, 0)
            Weight = ((Front_Out - Front) / 1728) * self.Density

            FrontList.append([Weight, Front_Out, (ECF1, EWF1, EDF1), Front])
        EndList = []

        for Combaination in self.SectionDict[1]:
            ECF2 = Combaination[0]
            EWF2 = Combaination[1]
            EDF2 = Combaination[2]

            End = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[1], self.SemiWidth[1],
                self.Length[1],
                ECF2, EWF2, EDF2,
                self.Length[1], 0)
            End_Out = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[1] + self.Thickness, self.SemiWidth[1] + self.Thickness,
                self.Length[1] + self.Thickness,
                ECF2, EWF2, EDF2,
                self.Length[1] + self.Thickness, 0)
            Weight = ((End_Out - End) / 1728) * self.Density

            EndList.append([Weight, End_Out, (ECF2, EWF2, EDF2), End])

        FrontList.sort(key=lambda x: x[0])
        EndList.sort(key=lambda x: x[0])

        indexF = 0
        indexE = 0
        lengthF = len(FrontList)
        lengthE = len(EndList)
        while (len(self.Top3) != 3):
            Weight = FrontList[indexF][0] + EndList[indexE][0]
            Capability = (FrontList[indexF][1] + EndList[indexE][1]) * 0.160111447518 * 0.225
            if (Capability > (Weight + self.CrewWeight)):
                ECF = [FrontList[indexF][2][0], EndList[indexE][2][0]]
                EWF = [FrontList[indexF][2][1], EndList[indexE][2][1]]
                EDF = [FrontList[indexF][2][2], EndList[indexE][2][2]]
                StryofoamVolume = self.Styrofoam_Volume_Calculate(self.operation_f, ECF, EWF, EDF) + \
                                  self.Styrofoam_Volume_Calculate(self.operation_e, ECF, EWF, EDF)
                ConcreteVolume = (Weight / self.Density) * 1728
                submerge = (StryofoamVolume + ConcreteVolume) * 0.160111447518 * 0.225
                if (submerge > Weight):
                    # Can be take into account
                    self.Top3.append([Weight, (ECF, EWF, EDF),
                                      (FrontList[indexF][-1], EndList[indexE][-1]),
                                      (FrontList[indexF][1], EndList[indexE][1])])
            if (indexF + 1 != lengthF):
                indexF += 1
            if (indexE + 1 != lengthE):
                indexE += 1
        self.ResultLog = len(FrontList) * len(EndList)

    def Optimzation_Threebody(self):
        FrontList = []
        for Combaination in self.SectionDict[0]:
            ECF1 = Combaination[0]
            EWF1 = Combaination[1]
            EDF1 = Combaination[2]

            Front = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[0], self.SemiWidth[0],
                (self.Length[0]),
                ECF1, EWF1, EDF1,
                self.Length[0], 0)
            Front_Out = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[0] + self.Thickness, self.SemiWidth[0] + self.Thickness,
                (self.Length[0] + self.Thickness),
                ECF1, EWF1, EDF1,
                self.Length[0] + self.Thickness, 0)
            Weight = ((Front_Out - Front) / 1728) * self.Density

            FrontList.append([Weight, Front_Out, (ECF1, EWF1, EDF1), Front])
        MidList = []
        for Combaination in self.SectionDict[1]:
            ECF2 = Combaination[0]
            EWF2 = Combaination[1]
            EDF2 = Combaination[2]

            # Get Basic Data
            if (self.Log[2] == 24):
                SWvalue = (self.SemiWidth[0]
                           / self.SemiWidth[1]) ** (1 / EWF2)
                SWvalue_O = ((self.SemiWidth[0] + self.Thickness)
                             / (self.SemiWidth[1] + self.Thickness)) ** (1 / EWF2)

                self.Length[1] = self.Length[1] - self.B2

                self.B2 = round((self.Length[1] * SWvalue) / (1 - SWvalue), 10)
                self.B2_O = round(((self.Length[1]) * SWvalue_O) / (1 - SWvalue_O), 10)
                self.B2_Diff = self.B2_O - self.B2

                self.Length[1] += self.B2

                Mid = OptimizationCalculation.QuickIntegralMethod_AssymetricB2(
                    self.Depth[1], self.SemiWidth[1],
                    self.Length[1],
                    ECF2, EWF2, EDF2,
                    self.Length[1], self.B2)
                Mid_Out = OptimizationCalculation.QuickIntegralMethod_AssymetricB2(
                    self.Depth[1] + self.Thickness, self.SemiWidth[1] + self.Thickness,
                    self.Length[1] + self.B2_Diff,
                    ECF2, EWF2, EDF2,
                    self.Length[1] + self.B2_Diff, self.B2_O)

            else:
                if (ECF2 == 0 and ECF2 == 0):
                    Mid = OptimizationCalculation.QuickIntegralMethod_constant(
                        self.Depth[1], self.SemiWidth[1], self.Length[1], ECF2, self.Length[1]
                    )
                    Mid_Out = OptimizationCalculation.QuickIntegralMethod_constant(
                        self.Depth[1] + self.Thickness,
                        self.SemiWidth[1] + self.Thickness, self.Length[1] + self.Thickness, ECF2,
                        self.Length[1] + self.Thickness
                    )



                else:
                    Mid = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                        self.Depth[1], self.SemiWidth[1],
                        self.Length[1],
                        ECF2, EWF2, EDF2,
                        self.Length[1], 0)
                    Mid_Out = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                        self.Depth[1] + self.Thickness, self.SemiWidth[1] + self.Thickness,
                        self.Length[1] + self.Thickness,
                        ECF2, EWF2, EDF2,
                        self.Length[1] + self.Thickness, 0)

            Weight = ((Mid_Out - Mid) / 1728) * self.Density

            MidList.append([Weight, Mid_Out, (ECF2, EWF2, EDF2), Mid])

        EndList = []
        for Combaination in self.SectionDict[2]:
            ECF3 = Combaination[0]
            EWF3 = Combaination[1]
            EDF3 = Combaination[2]

            End = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[2], self.SemiWidth[2],
                self.Length[2],
                ECF3, EWF3, EDF3,
                self.Length[2], 0)
            End_Out = OptimizationCalculation.QuickIntegralMethod_Inconstant(
                self.Depth[2] + self.Thickness, self.SemiWidth[2] + self.Thickness,
                self.Length[2] + self.Thickness,
                ECF3, EWF3, EDF3,
                self.Length[2] + self.Thickness, 0)
            Weight = ((End_Out - End) / 1728) * self.Density

            EndList.append([Weight, End_Out, (ECF3, EWF3, EDF3), End])

        FrontList.sort(key=lambda x: x[0])
        MidList.sort(key=lambda x: x[0])
        EndList.sort(key=lambda x: x[0])

        indexF = 0
        indexM = 0
        indexE = 0
        lengthF = len(FrontList)
        lengthM = len(MidList)
        lengthE = len(EndList)
        while (len(self.Top3) != 3):
            Weight = FrontList[indexF][0] + MidList[indexM][0] + EndList[indexE][0]
            Capability = (FrontList[indexF][1] + MidList[indexM][1] + EndList[indexE][1]) * 0.160111447518 * 0.225
            if (Capability > (Weight + self.CrewWeight)):
                ECF = [FrontList[indexF][2][0], MidList[indexM][2][0], EndList[indexE][2][0]]
                EWF = [FrontList[indexF][2][1], MidList[indexM][2][1], EndList[indexE][2][1]]
                EDF = [FrontList[indexF][2][2], MidList[indexM][2][2], EndList[indexE][2][2]]
                StryofoamVolume = self.Styrofoam_Volume_Calculate(self.operation_f, ECF, EWF, EDF) + \
                                  self.Styrofoam_Volume_Calculate(self.operation_e, ECF, EWF, EDF)
                ConcreteVolume = (Weight / self.Density) * 1728
                submerge = (StryofoamVolume + ConcreteVolume) * 0.160111447518 * 0.225
                if (submerge > Weight):
                    # Can be take into account
                    self.Top3.append([Weight, (ECF, EWF, EDF),
                                      (FrontList[indexF][-1], MidList[indexM][-1], EndList[indexE][-1]),
                                      (FrontList[indexF][1], MidList[indexM][1], EndList[indexE][1])])
            if (indexF + 1 != lengthF):
                indexF += 1
            if (indexM + 1 != lengthM):
                indexM += 1
            if (indexE + 1 != lengthE):
                indexE += 1

        self.ResultLog = len(MidList) * len(FrontList) * len(EndList)

    def Styrofoam_Volume_Calculate(self, op_list, ECF, EWF, EDF):
        volume = 0
        for op in op_list:
            num = op[0]
            CoverL = op[1]
            if (CoverL == 0):
                pass
            elif (self.Log[2] == 24):
                # canoe that are not asymmetric
                if (num == 1):
                    volume += OptimizationCalculation.QuickIntegralMethod_AssymetricB2(
                        self.Depth[num], self.SemiWidth[num], self.Length[num],
                        ECF[num], EWF[num], EDF[num],
                        self.B2 + CoverL, self.B2)
                else:
                    volume += OptimizationCalculation.QuickIntegralMethod_Inconstant(
                        self.Depth[num], self.SemiWidth[num], self.Length[num],
                        ECF[num], EWF[num], EDF[num],
                        CoverL, 0)
            else:
                if (EWF[num] == 0 and EDF[num] == 0):
                    volume += OptimizationCalculation.QuickIntegralMethod_constant(
                        self.Depth[num], self.SemiWidth[num], self.Length[num], ECF, CoverL)
                else:
                    volume += OptimizationCalculation.QuickIntegralMethod_Inconstant(
                        self.Depth[num], self.SemiWidth[num], self.Length[num],
                        ECF[num], EWF[num], EDF[num],
                        CoverL, 0)

        return volume

    def GenerateSection(self, ECurveF, sectionNum):
        for EWF in np.arange(self.CDDRange["Exponent of Width"][sectionNum][0],
                             self.CDDRange["Exponent of Width"][sectionNum][1],
                             self.CDDRange["Interval"]):
            for EDF in np.arange(self.CDDRange["Exponent of Depth"][sectionNum][0],
                                 self.CDDRange["Exponent of Depth"][sectionNum][1],
                                 self.CDDRange["Interval"]):
                self.SectionDict[sectionNum].append([ECurveF, EWF, EDF])

    @staticmethod
    def QuickIntegralMethod_Inconstant(depth, width, length, ECF, ECW, ECD, upper, lower):
        # Only Apply for the calculation of the canoe volume
        # Consider the Quick Integral expansion Volume formula for Bow to be:
        """
        .. math:: \frac{2*a*d*w*l^{-b-c}\left(u^{b+c+1}-o^{b+c+1}\right)}{\left(a+1\right)\left(b+c+1\right)}
        """
        IntegralEXP = (ECD + ECW + 1)
        Result = (2 * ECF * depth * width * (length ** (-ECW - ECD)) * (
                (upper ** (IntegralEXP)) - (lower ** (IntegralEXP)))) / ((ECF + 1) * (IntegralEXP))
        return Result

    @staticmethod
    def QuickIntegralMethod_AssymetricB2(depth, width, length, ECF, ECW, ECD, upper, lower):
        # Consider Function to be \frac{2adw\left(u^k-o^k\right)}{l^b\left(a+1\right)k}
        IntegralEXP = (ECW + 1)
        Result = (2 * ECF * depth * width * ((upper ** (IntegralEXP)) - (lower ** (IntegralEXP)))) \
                 / ((ECF + 1) * (length ** (ECW)) * (IntegralEXP))
        return Result

    @staticmethod
    def QuickIntegralMethod_constant(depth, width, length, ECF, upper):
        Result = (2 * length * width * ECF * (upper ** ((ECF + 1) / ECF))) / \
                 ((depth ** (1 / ECF)) * (ECF + 1))
        return Result

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
            elif (canoe_cover < length_list[0] and lenIndex - 1 == 0):
                return [[0, canoe_cover]]  # if the cover is less than the first length

        return calculation_operation_list
