import math
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from scipy.integrate import quad
from stl import mesh
from sympy import *


class Calculation():

    def __init__(self, CanoeDataBase_Object):
        self.SymmetryBoolean = False
        print("Calculation Work")

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

        self.CanoeVolume = 0
        self.CanoeWeight = 0
        self.TotalWeight = 0
        self.SubmergeBoolean = 0
        self.FlowBoolean = 0
        self.Buoyancy = 0
        self.Buoyancy_Submerge = 0
        self.Symmetricity = self.CalculationObject.GetSYM()

        self.Note = []
        self.NoteMenu = {0: "Set Deign -> One Body", 1: "Set Deign -> Two Body", 2: "Set Deign -> Three Body",
                         10: "Set Deign SubProperty -> Symmetric", 11: "Set Deign SubProperty -> Asymmetric",
                         20: "Assign HullType -> Symmetric Hull", 21: "Assign HullType -> LongShort Hull",
                         22: "Assign HullType -> Symmetric Constant Hull",
                         23: "Assign HullType -> Asymmetric Constant Hull",
                         24: "Assign HullType -> Asymmetric Hull"}

        self.SignData()

    def SignData(self):
        SDD, HDD = self.CalculationObject.GetData_CDD()
        # Write Function for generate testprofile
        # with open("SDDHDD",'w') as file: file.write(str([SDD,HDD]))

        for v in SDD.values():
            self.Length.append(v[0])
            self.Width.append(v[1])
            self.SemiWidth.append(v[1] / 2)
            self.Depth.append(v[2])
            self.ECurveF.append(v[3])
            self.EWidthF.append(v[4])
            self.EDepthF.append(v[5])

        self.CoverLength = HDD[0]
        self.Density = HDD[1]
        self.Thickness = HDD[2]
        self.CrewWeight = HDD[3]

        self.Num = len(self.Length)

        self.SignFunction_Main()

    def CalDataReturn(self):
        if (self.SymmetryBoolean == True):
            self.Note.insert(1, 10)
        elif (self.SymmetryBoolean == False):
            self.Note.insert(1, 11)
        # Print the OperationNote
        for num in self.Note:
            print(self.NoteMenu[num])

    def SignFunction_Main(self):

        if (len(self.ECurveF) == 1):
            self.Note.append(0)
            self.SignFunction_SymmetryHull()

        elif (len(self.ECurveF) == 2):
            self.Note.append(1)
            self.SignFunction_TwoBodyHull()

        elif (len(self.ECurveF) == 3):
            self.Note.append(2)
            self.SignFunction_ThreeBodyHull()

    def BuildLambad_Depth(self, index):
        return (lambda x: self.Depth[index] * (x / self.Length[index]) ** self.EDepthF[index])

    def BuildLambad_Depth_O(self, index):

        return (lambda x: (self.Depth[index] + self.Thickness) * (x / (self.Length[index] + self.Thickness)) **
                          self.EDepthF[index])

    def BuildLambad_Depth_O_A(self, index):
        return (
            lambda x: (self.Depth[index] + self.Thickness) * (x / (self.Length[index] + self.B2_Diff)) ** self.EDepthF[
                index])

    def BuildLambad_Depth_Semi(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: self.Depth[0] * (x / SemiLength) ** self.EDepthF[0])

    def BuildLambad_Width(self, index):
        return (lambda x: self.SemiWidth[index] * (x / self.Length[index]) ** self.EWidthF[index])

    def BuildLambad_Width_O(self, index):
        return (lambda x: (self.SemiWidth[index] + self.Thickness) * (x / (self.Length[index] + self.Thickness)) **
                          self.EWidthF[index])

    def BuildLambad_Width_O_A(self, index):
        return (lambda x: (self.SemiWidth[index] + self.Thickness) * (x / (self.Length[index] + self.B2_Diff)) **
                          self.EWidthF[index])

    def BuildLambad_Width_Semi(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: self.SemiWidth[0] * (x / SemiLength) ** self.EWidthF[0])

    def BuildLambad_Width_Semi_O(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: (self.SemiWidth[0] + self.Thickness) * (x / (SemiLength + self.Thickness)) ** self.EWidthF[0])

    def BuildLambad_Depth_Semi_O(self):
        SemiLength = self.Length[0] / 2
        return (lambda x: (
                                  self.Depth[0] + self.Thickness) * (x / (SemiLength + self.Thickness)) ** self.EDepthF[
                              0])

    def DataPrint(self):
        print(self.Length)
        print(self.Width)
        print(self.SemiWidth)
        print(self.Depth)

        print(self.ECurveF)
        print(self.EWidthF)
        print(self.EDepthF)

    def SignFunction_SymmetryHull(self):
        self.Note.append(20)
        self.DataPrint()

        self.SymmetryBoolean = True

        self.WidthFList.append(self.BuildLambad_Width_Semi()
                               )
        self.WidthFList_Outside.append(self.BuildLambad_Width_Semi_O())
        self.DepthFList.append(self.BuildLambad_Depth_Semi()
                               )
        self.DepthFList_Outside.append(self.BuildLambad_Depth_Semi_O())

    def SignFunction_TwoBodyHull(self):
        self.DataPrint()

        if (self.Length[0] == self.Length[1] and self.SemiWidth[0] == self.SemiWidth[1] and self.Depth[0] == self.Depth[
            1] and self.EWidthF[0] == self.EWidthF[1] and self.EDepthF[0] == self.EDepthF[1]):
            self.SymmetryBoolean = True
            self.Note.append(20)
        else:
            self.Note.append(21)

        for index in range(0, len(self.EDepthF)):
            self.WidthFList.append(self.BuildLambad_Width(index))
            self.WidthFList_Outside.append(self.BuildLambad_Width_O(index))
            self.DepthFList.append(self.BuildLambad_Depth(index)
                                   )
            self.DepthFList_Outside.append(self.BuildLambad_Depth_O(index)
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
        self.DataPrint()
        if (SBoolean == True):
            self.Note.append(22)
        elif (SBoolean == False):
            self.Note.append(23)

        for index in range(0, len(self.EDepthF)):
            if (self.EWidthF[index] != 0 and self.EDepthF[index] != 0):
                self.WidthFList.append(self.BuildLambad_Width(index))
                self.WidthFList_Outside.append(self.BuildLambad_Width_O(index))
                self.DepthFList.append(self.BuildLambad_Depth(index)
                                       )
                self.DepthFList_Outside.append(self.BuildLambad_Depth_O(index)
                                               )
            elif (self.EWidthF[index] == 0 and self.EDepthF[index] == 0):
                self.WidthFList.append(-1)
                self.WidthFList_Outside.append(-1)
                self.DepthFList.append(-1)
                self.DepthFList_Outside.append(-1)

    def SignFunction_ThreeBodyHUll_Asymmetric(self):
        self.Note.append(24)
        # Confirm Cross-sectional data for Middle Section
        self.Set_FormulaPoint_Asymmetric()
        self.Length[1] = self.Length[1] + self.B2
        # Pair Back section base on the Middle
        self.Width[2] = self.Width[1]
        self.Depth[2] = self.Depth[1]
        self.SemiWidth[2] = self.SemiWidth[1]
        self.DataPrint()
        # Sign Function for Front

        self.WidthFList.append(
            self.BuildLambad_Width(0))
        self.WidthFList_Outside.append(
            self.BuildLambad_Width_O(0))
        self.DepthFList.append(self.BuildLambad_Depth(0)
                               )
        self.DepthFList_Outside.append(self.BuildLambad_Depth_O(0))

        # Sign Function for Middle

        self.WidthFList.append(
            self.BuildLambad_Width(1))
        self.WidthFList_Outside.append(
            self.BuildLambad_Width_O_A(1))
        self.DepthFList.append(self.Depth[1])
        self.DepthFList_Outside.append((self.Depth[1]+self.Thickness))

        # Sign Function for end

        self.WidthFList.append(
            self.BuildLambad_Width(2))
        self.WidthFList_Outside.append(
            self.BuildLambad_Width_O(2))
        self.DepthFList.append(self.BuildLambad_Depth(2)
                               )
        self.DepthFList_Outside.append(self.BuildLambad_Depth_O(2))

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

    def Canoe_Volume(self):

        SwDFunction_List = []
        SwD_Out_Function_List = []
        Volume_Inside_List = []
        Volume_Outside_List = []
        Volume_Inside = 0
        Volume_Outside = 0

        if (self.Note[2] != 24):
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

            if (len(self.WidthFList) == 1 and len(self.DepthFList) == 1):

                Volume_Inside_List.append(2 * 2
                                          * ((self.ECurveF[0]) / (self.ECurveF[0] + 1))
                                          * quad(SwDFunction_List[0], 0, self.Length[0] / 2)[0])
                Volume_Outside_List.append(2 * 2
                                           * ((self.ECurveF[0]) / (self.ECurveF[0] + 1))
                                           * quad(SwD_Out_Function_List[0], 0, self.Length[0] / 2 + self.Thickness)[0])

            elif (len(self.WidthFList) != 1 and len(self.DepthFList) != 1):
                for index in range(0, len(self.WidthFList)):
                    if (self.WidthFList[index] == -1 and self.DepthFList[index] == -1):
                        Volume_Inside_List.append(
                            self.Length[index] * 2 * quad(SwDFunction_List[index], 0, self.Depth[index])[0])
                        Volume_Outside_List.append(
                            self.Length[index] * 2 *
                            quad(SwD_Out_Function_List[index], 0, (self.Depth[index] + self.Thickness))[0])
                    elif (self.WidthFList[index] != -1 and self.DepthFList[index] != -1):
                        Volume_Inside_List.append(
                            2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) *
                            quad(SwDFunction_List[index], 0, self.Length[index])[0])
                        Volume_Outside_List.append(2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * quad(
                            SwD_Out_Function_List[index], 0, self.Length[index] + self.Thickness)[0])
        elif (self.Note[2] == 24):

            for k in range(0, len(self.WidthFList)):
                if(k == 1):
                    SwDFunction_List.append(self.Sign_CurveFormula_A(k))
                    SwD_Out_Function_List.append(
                        self.Sign_CurveFormula_Out_A(k))

                else:
                    SwDFunction_List.append(self.Sign_CurveFormula(k))
                    SwD_Out_Function_List.append(
                        self.Sign_CurveFormula_Out(k))



            for index in range(0, len(self.WidthFList)):
                if (index == 1):
                    Volume_Inside_List.append(
                        2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * self.Depth[index]*
                        quad(self.WidthFList[index], self.B2, self.Length[index] + self.B2)[0])
                    Volume_Outside_List.append(
                        2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) *
                        (self.Depth[index]+self.Thickness)*
                        quad(self.WidthFList_Outside[index], self.B2_O, self.Length[index] + self.B2_O)[0])

                if (index != 1):
                    Volume_Inside_List.append(
                        2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) *
                        quad(SwDFunction_List[index], 0, self.Length[index])[0])
                    Volume_Outside_List.append(2 * ((self.ECurveF[index]) / (self.ECurveF[index] + 1)) * quad(
                        SwD_Out_Function_List[index], 0, self.Length[index] + self.Thickness)[0])

        for i, j in zip(Volume_Inside_List, Volume_Outside_List):
            Volume_Inside += i
            Volume_Outside += j
        Concrete_Volume = Volume_Outside - Volume_Inside
        print(Volume_Inside)
        print(Volume_Outside)
        print(Concrete_Volume)

    def Styrofoam_Volume(self):
        print("k")

    # Model Construction

    def Model_Generate(self):
        if (len(self.Length) == 1):
            self.Symmetriclize()

        interval = 1

        V_List = self.Mesh_Generate()
        if (self.Note[2] == 24):
            # minus the B2
            self.Length[1] = self.Length[1] - self.B2
        CoverList = [self.CoverLength - self.Thickness, self.CoverLength,
                     sum(self.Length) - self.CoverLength + self.Thickness * 2,
                     sum(self.Length) - self.CoverLength + self.Thickness * 3]

        Index_Set = []

        for FLBL in CoverList:
            Vertex_I, Vertex_O, LenList = self.Vertex_Generating(V_List)
            Set_Index = self.PairCoverLength(LenList, FLBL)
            Index_Set.append(Set_Index[2])
            if (Set_Index[0] == True):
                formula, W = self.Single_Formula_Generate(
                    self.CoverLength, Set_Index[1])
                X, Y, Z = self.CrossSection_Coordinate_Generate(
                    W, interval, formula, FLBL, "3D")
                Format = self.XYZ_Format_Generating(X, Y, Z, Set_Index[1])
                V_List[0].insert(Set_Index[2], Format)

        Face_List = []
        Face_Num = 0

        for Number, V_set in enumerate(V_List):
            F_L = []
            for add in range(len(V_set[1]) - 1):
                V_set[0].append(V_set[0][0])
                V_set[-1].append(V_set[-1][0])
            for C_Index in range(1, len(V_set)):
                inner = V_set[C_Index - 1]
                outter = V_set[C_Index]
                Point4_Set = []

                if (Number == 1):
                    for P4 in range(1, len(inner)):
                        Point4_Set.append(
                            [inner[P4 - 1], inner[P4], outter[P4 - 1], outter[P4]])
                    F_L.append(Point4_Set)
                if (Number == 0):
                    if (outter[0][2] > CoverList[1] and outter[0][2] <= CoverList[2]):

                        for P4 in range(1, len(inner)):
                            Point4_Set.append(
                                [inner[P4], inner[P4 - 1],
                                 outter[P4], outter[P4 - 1]])
                        F_L.append(Point4_Set)
                    if (outter[0][2] <= CoverList[1] or outter[0][2] > CoverList[2]):
                        for P4 in range(1, len(inner)):
                            Point4_Set.append(
                                [inner[P4 - 1], inner[P4],
                                 outter[P4 - 1], outter[P4]])
                        F_L.append(Point4_Set)

            Face_List.append(F_L)

        Inter, Cover, Cover_H = self.Vertical_Horizontal_Mesh_Generate(
            V_List, Index_Set)
        Face_List.append(Inter)
        Face_List.append(Cover)
        Face_List.append(Cover_H)

        for l in Face_List:
            for p in l:
                Face_Num += len(p) * 2

        # Sign Front and Back

        cube = mesh.Mesh(np.zeros(Face_Num, dtype=mesh.Mesh.dtype))

        # Resigning the Coordinate

        face_Counter = 0
        for list in Face_List:
            for face in list:
                for set in face:
                    # Sign Two faces
                    for num in range(3):
                        cube.vectors[face_Counter][num] = set[num]
                        cube.vectors[face_Counter + 1][num] = set[(num + 1) * -1]

                    face_Counter += 2

        cube.rotate([0.0, 0.5, 0.0], math.radians(90))
        cube.rotate([0.5, 0.0, 0.0], math.radians(-1 * 90))

        cube.save('Canoe.stl')

        print("Model Generated")
        # For Debug

        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        # Render the cube
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))

        # Auto scale to the mesh size
        scale = cube.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)
        axes.set_xlabel("X axis")
        axes.set_ylabel("Y axis")
        axes.set_zlabel("Z axis")

        # Show the plot to the screen
        pyplot.show()



    def Coordinatie_Generate(self, ModeString):
        global L_index
        SymX = Symbol('x')
        # The list that save the curve function for each 0.1 inch in length
        CurveList_Inside, CurveList_Outside = self.Formula_Generate()

        Coordinate_Inside = []
        Coordinate_Outside = []

        interval = 1

        Z_value = 0
        Z_value_O = 0

        for num in range(0, self.Num):

            CI_List = []
            CO_List = []
            for dataIndex in range(0, len(CurveList_Inside[num])):
                if (num == 1 and dataIndex == 0):
                    Z_value -= interval
                if (self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):

                    for L_index in np.arange(0, self.Length[num], interval):

                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(

                            CurveList_Inside[num][dataIndex][1], interval, CurveList_Inside[num][dataIndex][0], Z_value,
                            ModeString)
                        CI_List.append([X_List, Y_List, Z_List])
                        if (L_index + interval >= self.Length[num]):
                            X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                CurveList_Inside[num][dataIndex][1], interval, CurveList_Inside[num][dataIndex][0],
                                Z_value + interval, ModeString)
                            CI_List.append([X_List, Y_List, Z_List])
                        Z_value += interval

                    if (L_index + interval >= self.Length[num]):
                        Z_value -= interval

                elif (self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):
                    if (CurveList_Inside[num][dataIndex][0] == 0):
                        CI_List.append([[0], [0], [Z_value]])

                    elif (CurveList_Inside[num][dataIndex][0] != 0):

                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList_Inside[num][dataIndex][1], interval, CurveList_Inside[num][dataIndex][0], Z_value,
                            ModeString)
                        CI_List.append([X_List, Y_List, Z_List])
                        if (num == 1 and dataIndex + interval >= len(CurveList_Inside[num])):
                            Z_value -= interval
                Z_value += interval

            for dataIndex_O in range(0, len(CurveList_Outside[num])):
                if (num == 1 and dataIndex_O == 0):
                    Z_value_O -= interval
                if (self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):
                    for L_Index_O in np.arange(0, self.Length[num], interval):
                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0],
                            Z_value_O, ModeString)
                        CO_List.append([X_List, Y_List, Z_List])
                        if (L_Index_O + interval >= self.Length[num]):
                            X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                CurveList_Outside[num][dataIndex_O][1], interval,
                                CurveList_Outside[num][dataIndex_O][0], Z_value_O + interval, ModeString)
                            CO_List.append([X_List, Y_List, Z_List])

                        Z_value_O += interval
                        if (L_Index_O + interval >= self.Length[num]):
                            Z_value_O -= interval

                elif (self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):

                    if ((dataIndex_O == len(CurveList_Outside[num]) - 1 and num == 0) or (
                            dataIndex_O == 0 and num == len(self.Length) - 1)):

                        if (num == 0 and dataIndex_O == len(CurveList_Outside[num]) - 1):
                            Z_value_O += self.Thickness - interval
                            if (CurveList_Outside[num][dataIndex_O][0] != 0):
                                X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                    CurveList_Outside[num][dataIndex_O][1], interval,
                                    CurveList_Outside[num][dataIndex_O][0], Z_value_O, ModeString)
                                CO_List.append([X_List, Y_List, Z_List])
                        elif (num == len(self.Length) - 1 and dataIndex_O == 0):

                            if (CurveList_Outside[num][dataIndex_O][0] != 0):
                                X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                    CurveList_Outside[num][dataIndex_O][1], interval,
                                    CurveList_Outside[num][dataIndex_O][0], Z_value_O, ModeString)
                                CO_List.append([X_List, Y_List, Z_List])
                                Z_value_O += self.Thickness - interval

                    elif (CurveList_Outside[num][dataIndex_O][0] != 0 and dataIndex_O + interval <= len(
                            CurveList_Outside[num])):
                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0],
                            Z_value_O, ModeString)
                        CO_List.append([X_List, Y_List, Z_List])
                        if (num == 1 and float(dataIndex_O + interval) == float(len(CurveList_Outside[num]))):
                            Z_value_O -= interval

                    elif (CurveList_Outside[num][dataIndex_O][0] == 0):
                        CO_List.append([[0], [0], [Z_value_O]])

                Z_value_O += interval

            Coordinate_Inside.append(CI_List)
            Coordinate_Outside.append(CO_List)

        # Used to Debug

        """
        print("First Section")

        for i, j in zip(Coordinate_Inside[0], CurveList_Inside[0]):
            print("Inside Fucnction: %s" % (j[0]))
            print("\n")
            for a, b, c in zip(i[0], i[1], i[2]):
                print("X: %s || Y: %s || Z: %s" % (a, b, c))
            print("\n")

        print("Second Section")

        for i, j in zip(Coordinate_Inside[1], CurveList_Inside[1]):
            print("Inside Fucnction: %s" % (j[0]))
            for a, b, c in zip(i[0], i[1], i[2]):
                print("X: %s || Y: %s || Z: %s" % (a, b, c))
            print("\n")





        print("Third Section")


        for i, j in zip(Coordinate_Inside[2], CurveList_Inside[2]):
            print("Inside Fucnction: %s" % (j[0]))
            print("\n")
            for a, b, c in zip(i[0], i[1], i[2]):
                print("X: %s || Y: %s || Z: %s" % (a, b, c))
            print("\n")

        print(len(Coordinate_Inside[0]))
        print(len(Coordinate_Inside[1]))
        print(len(Coordinate_Inside[2]))





        print("First Section")

        for i, j in zip(Coordinate_Outside[0], CurveList_Outside[0]):
            print("Outside Fucnction: %s" % (j[0]))
            print("\n")
            for a, b, c in zip(i[0], i[1], i[2]):
                print("X: %s || Y: %s || Z: %s" % (a, b, c))
            print("\n")

        print("Second Section")

        for i in Coordinate_Outside[1]:
            for a, b, c in zip(i[0], i[1], i[2]):
                print("X: %s || Y: %s || Z: %s" % (a, b, c))
            print("\n")




        print("Third Section")

        for i, j in zip(Coordinate_Outside[2], CurveList_Outside[2]):
            print("Outside Fucnction: %s" % (j[0]))
            print("\n")
            for a, b, c in zip(i[0], i[1], i[2]):
                print("X: %s || Y: %s || Z: %s" % (a, b, c))
            print("\n")

        print(len(Coordinate_Outside[0]))
        print(len(Coordinate_Outside[1]))
        print(len(Coordinate_Outside[2]))

        """

        return (Coordinate_Inside, Coordinate_Outside)


    def Formula_Generate(self):
        CurveFbyInch_Inside = []
        CurveFbyInch_Outside = []

        SymX = Symbol('x')
        interval = 1
        for num in range(self.Num):
            CL_In = []
            CL_Out = []

            if (self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):
                CL_In = [[self.Depth[num] * (SymX / self.SemiWidth[num])
                          ** self.ECurveF[num], self.SemiWidth[num], self.Depth[num]]]
                CL_Out = [[(self.Depth[num] + self.Thickness) * (SymX / (self.SemiWidth[num] + self.Thickness))
                           ** self.ECurveF[num], (self.SemiWidth[num] + self.Thickness),
                           (self.Depth[num] + self.Thickness)]]

            elif (self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0 and self.Num == 3 and num == 1):
                for length in np.arange(self.B2, self.Length[num], interval):

                    Width = self.WidthFList[num](length)
                    Depth = self.Depth[1]

                    CL_In.append(
                        [Depth * (SymX / Width) ** self.ECurveF[num], Width, Depth])
                    if (length + interval >= self.Length[num]):
                        Width = self.WidthFList[num](self.Length[num])
                        CL_In.append(
                            [Depth * (SymX / Width) ** self.ECurveF[num], Width, Depth])

                for length_out in np.arange(self.B2_O, self.Length[num] + self.B2_Diff, interval):
                    Width_O = self.WidthFList_Outside[num](length_out)
                    Depth_O = self.Depth[1] + self.Thickness

                    CL_Out.append(
                        [Depth_O * (SymX / Width_O) ** self.ECurveF[num], Width_O, Depth_O])

                    if (length_out + interval >= self.Length[num] + self.B2_Diff):
                        Width_O = self.WidthFList_Outside[num](
                            self.Length[num] + self.B2_Diff)
                        CL_Out.append(
                            [Depth_O * (SymX / Width_O) ** self.ECurveF[num], Width_O, Depth_O])

            elif (self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):

                for length in np.arange(0, self.Length[num], interval):
                    Width = self.WidthFList[num](length)
                    Depth = self.DepthFList[num](length)

                    CL_In.append(
                        [Depth * (SymX / Width) ** self.ECurveF[num], Width, Depth])
                    if (length + interval >= self.Length[num]):
                        Width = self.WidthFList[num](self.Length[num])
                        Depth = self.DepthFList[num](self.Length[num])
                        CL_In.append(
                            [Depth * (SymX / Width) ** self.ECurveF[num], Width, Depth])

                for length_out in np.arange(0, self.Length[num] + self.Thickness, interval):
                    Width_O = self.WidthFList_Outside[num](length_out)
                    Depth_O = self.DepthFList_Outside[num](length_out)

                    CL_Out.append(
                        [Depth_O * (SymX / Width_O) ** self.ECurveF[num], Width_O, Depth_O])

                    if (length_out + interval >= self.Length[num] + self.Thickness):
                        Width_O = self.WidthFList_Outside[num](
                            self.Length[num] + self.Thickness)
                        Depth_O = self.DepthFList_Outside[num](
                            self.Length[num] + self.Thickness)
                        CL_Out.append(
                            [Depth_O * (SymX / Width_O) ** self.ECurveF[num], Width_O, Depth_O])

            CurveFbyInch_Inside.append(CL_In)
            CurveFbyInch_Outside.append(CL_Out)

        # reverse the end to make it pare with the canoe body
        CurveFbyInch_Inside[-1].reverse()
        CurveFbyInch_Outside[-1].reverse()

        # Use For Debug
        """
        for i in CurveFbyInch_Inside:
            for a in i:
                print("Curve Inside : %s"%(a))
            print("SectionLength:%s"%(len(i)))


        for i in CurveFbyInch_Outside:
            for a in i:
                print("Curve Outside : %s"%(a))
            print("SectionLength:%s"%(len(i)))
        """

        return (CurveFbyInch_Inside, CurveFbyInch_Outside)

    # Model Construction tools

    def XYZ_Format_Generating(self, X, Y, Z, num):

        Formate = []
        for x, y, z in zip(X, Y, Z):
            add = (self.Depth[num] + self.Thickness) - Y[-1]
            Formate.append([x, y + add, z])

        return (Formate)

    def Vertex_Generating(self, V_List):
        Vertex_I = []
        Vertex_O = []
        Length_List = []
        # Get Vectors for Inside and Outside
        for VI in V_List[0]:
            Vertex_I.append([VI[0], VI[-1]])
        for VO in V_List[1]:
            Vertex_O.append([VO[0], VO[-1]])

        for index in range(0, len(Vertex_I)):
            # X,Y,Z
            Length_List.append(Vertex_I[index][0][2])

        return (Vertex_I, Vertex_O, Length_List)

    def PairCoverLength(self, LenList, find):
        Diff = math.inf
        Sign_Boolean = False
        ReturnSet = []

        Sum = 0
        Len_Sum = [0]
        for length in self.Length:
            Sum += length
            Len_Sum.append(Sum)

        FindSign = find not in LenList
        if (FindSign == False):
            print("in")
            ReturnSet.append(Sign_Boolean)
            for num in range(1, len(Len_Sum)):
                if (find > Len_Sum[num - 1] and find <= Len_Sum[num]):
                    ReturnSet.append(num - 1)
            ReturnSet.append(LenList.index(find))
            print(ReturnSet)
            return (ReturnSet)
        if (FindSign == True):
            print("Not in")
            Sign_Boolean = True
            ReturnSet.append(Sign_Boolean)
            for num in range(1, len(Len_Sum)):
                if (find > Len_Sum[num - 1] and find <= Len_Sum[num]):
                    ReturnSet.append(num - 1)
            LenList.append(find)
            LenList.sort()
            ReturnSet.append(LenList.index(find))
            print(ReturnSet)
            return (ReturnSet)

    def Vertical_Horizontal_Mesh_Generate(self, V_List, IndexSet):
        Vertex_I = []
        Vertex_O = []

        F_L = []
        F_L1 = []
        F_L2 = []
        LP = []
        LN = []

        # Get Vectors for Inside and Outside
        for VI in V_List[0]:
            Vertex_I.append([VI[0], VI[-1]])
        for VO in V_List[1]:
            Vertex_O.append([VO[0], VO[-1]])

        for add in range(int((len(Vertex_O) - len(Vertex_I)) / 2)):
            print("Add_I")
            Vertex_I.append(Vertex_I[-1])
            Vertex_I.insert(0, Vertex_I[0])
            IndexSet[0] = IndexSet[0] + 1
            IndexSet[1] = IndexSet[1] + 1

        for add in range(int((len(Vertex_I) - len(Vertex_O)) / 2)):
            print("Add_O")
            Vertex_O.append(Vertex_O[-1])
            Vertex_O.insert(0, Vertex_O[0])

        print(len(Vertex_I))
        print(len(Vertex_O))

        for index in range(1, len(Vertex_I)):
            F_L.append([[Vertex_I[index][0], Vertex_I[index - 1][0],
                         Vertex_O[index][0], Vertex_O[index - 1][0]]])
            F_L.append([[Vertex_I[index - 1][1], Vertex_I[index][1],
                         Vertex_O[index - 1][1], Vertex_O[index][1]]])

        for set in Vertex_I:
            LP.append(set[1])
            LN.append(set[0])

        for index in range(1, IndexSet[1] + 1):
            F_L1.append([[LP[index], LP[index - 1], LN[index], LN[index - 1]]])
        for index in range(IndexSet[2] + 1, len(LP)):
            F_L1.append([[LP[index], LP[index - 1], LN[index], LN[index - 1]]])

        for Number, I in enumerate(IndexSet):
            CN = []
            CP = []
            for Coordinate in V_List[0][I]:
                if (Coordinate[0] <= 0.0):
                    CN.append(Coordinate)
                if (Coordinate[0] >= 0.0):
                    CP.append(Coordinate)
            CP.reverse()
            Set = []
            if (Number == 1 or Number == 3):

                for Index in range(1, len(CP)):
                    Set.append([CP[Index], CP[Index - 1],
                                CN[Index], CN[Index - 1]])
                F_L2.append(Set)
            if (Number == 2 or Number == 0):
                for Index in range(1, len(CP)):
                    Set.append([CP[Index - 1], CP[Index],
                                CN[Index - 1], CN[Index]])

                F_L2.append(Set)

        return (F_L, F_L1, F_L2)

    def Mesh_Generate(self):
        CI, CO = self.Coordinatie_Generate("3D")

        Vectors_I = []
        Vectors_O = []

        for num in range(0, self.Num):
            for c_set in CI[num]:
                Set = []
                # For Debug
                """print("X:%s || Y:%s || Z:%s"%(c_set[0][0], c_set[1][0], c_set[2][0]))"""
                for x, y, z in zip(c_set[0], c_set[1], c_set[2]):
                    add = (self.Depth[num] + self.Thickness) - c_set[1][-1]
                    Set.append([x, y + add, z + self.Thickness])
                    """print(f"[{x},{y+add},{z+self.Thickness}]")"""
                Vectors_I.append(Set)

            for c_set_o in CO[num]:
                Set = []
                # For Debug
                """print("X_O:%s || Y_O:%s || Z_O:%s"%(c_set_o[0][0], c_set_o[1][0], c_set_o[2][0]))"""
                for x, y, z in zip(c_set_o[0], c_set_o[1], c_set_o[2]):
                    add = (self.Depth[num] + self.Thickness) - c_set_o[1][-1]
                    Set.append([x, y + add, z])
                Vectors_O.append(Set)
        return ([Vectors_I, Vectors_O])

    def Single_Formula_Generate(self, ZLength, num):
        SymX = Symbol('x')

        print(num)
        F1 = self.WidthFList[num]
        F2 = self.DepthFList[num]

        if (F1 == -1):
            def F1(x): return self.SemiWidth[num]

        if (F2 == -1):
            def F2(x): return self.Depth[num]

        Width = F1(ZLength)
        Depth = F2(ZLength)

        return (Depth * (SymX / Width) ** self.ECurveF[num], Width)

    def CrossSection_Coordinate_Generate(self, width, interval, function, zvalue, ModeString):

        xlist = []
        ylist = []
        zlist = []
        nxlist = []

        SymX = Symbol('x')

        if (ModeString == "3D"):
            # Find the largest Width, confirm the Width step interval
            Max_Width = max(self.Width)

            L_Width = Max_Width
            step_interval = width / L_Width

            for i in range(0, int(L_Width) + 1):
                w = step_interval * i

                xlist.append(w)
                ylist.append(function.subs(SymX, w))
                zlist.append(zvalue)

                if (w < width and (i + 1) * step_interval > width and int(L_Width) < Max_Width):
                    xlist.append(width)
                    ylist.append(function.subs(SymX, width))
                    zlist.append(zvalue)

        elif (ModeString == "Construction"):
            for i in np.arange(0, width, interval):

                xlist.append(i)
                ylist.append(function.subs(SymX, i))
                zlist.append(zvalue)

                if (i + interval >= width):
                    xlist.append(width)
                    ylist.append(function.subs(SymX, width))
                    zlist.append(zvalue)

        nxlist = xlist[1:]

        for x, y in zip(nxlist, ylist[1:]):
            xlist.insert(0, x * -1)
            ylist.insert(0, y)
            zlist.append(zvalue)

        return (xlist, ylist, zlist)

    def Symmetriclize(self):
        print("Being Symmetriclize")
        self.Num += 1
        self.Length.append(self.Length[0] / 2)
        self.Length[0] = self.Length[1]
        self.Width.append(self.Width[0])
        self.SemiWidth.append(self.SemiWidth[0])
        self.Depth.append(self.Depth[0])
        self.ECurveF.append(self.ECurveF[0])
        self.EWidthF.append(self.EWidthF[0])
        self.EDepthF.append(self.EDepthF[0])

        self.WidthFList.append(self.WidthFList[0])
        self.WidthFList_Outside.append(self.WidthFList_Outside[0])
        self.DepthFList.append(self.DepthFList[0])
        self.DepthFList_Outside.append(self.DepthFList_Outside[0])

        print(self.Length)
        print(self.Width)
        print(self.SemiWidth)
        print(self.Depth)

        print(self.ECurveF)
        print(self.EWidthF)
        print(self.EDepthF)
