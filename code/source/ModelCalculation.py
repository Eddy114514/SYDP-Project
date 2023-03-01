import copy
import math
import numpy as np
from stl import mesh
from typing import Union, Any

from Calculation import Calculation


class ModelCalculation(Calculation):
    def __init__(self, CDD):
        super().__init__(CDD)
        self.SignData()
        self.Inside_LengthList = []
        self.Outside_LengthList = []
        self.CoverLength_end = sum(self.Length) - self.CoverLength
        self.Inside_Length = []
        self.Outside_Length = []
        if (len(self.Length) == 1):
            self.Symmetriclize()
        self.LengthIndexGenerate()

    # Model Construction

    def Model_Generate(self):

        V_List = self.Mesh_Generate()
        if (self.Log[2] == 24):
            # minus the B2
            self.Length[1] = self.Length[1] - self.B2

        Vertext_In_Set, Vertext_Out_Set, Vertext_Out_Set_Cover = self.Vertex_Generating(V_List)

        Face_List = self.Hall_Mesh_Generate(V_List)
        Inside_Outside_Connection = self.Connection_Mesh_Generate(Vertext_In_Set, Vertext_Out_Set)
        Face_List.append(Inside_Outside_Connection)
        if (not self.FSDMode):
            # Only for normal model that require cover, vertical cover.
            Cover_Vertical, Cset_Vertical_List = self.Vertical_Cover_Mesh_Generate([V_List[0][0], V_List[0][-1]])

            Horizontal_Cover = self.Horizontal_Cover_Mesh_Generate(Vertext_Out_Set_Cover)

            Face_List.append(Cover_Vertical)

            Face_List.append(Horizontal_Cover)

        Face_Num = 0
        for l in Face_List:
            for p in l:
                Face_Num += len(p) * 2

        # Sign Front and Back

        canoe = mesh.Mesh(np.zeros(Face_Num, dtype=mesh.Mesh.dtype))

        # Resigning the Coordinate

        face_Counter = 0
        for face_sub_list in Face_List:
            for face in face_sub_list:
                for two_traingle_set in face:
                    # Sign Two faces
                    for num in range(3):
                        canoe.vectors[face_Counter][num] = two_traingle_set[num]
                        canoe.vectors[face_Counter + 1][num] = two_traingle_set[(num + 1) * -1]

                    face_Counter += 2
        # To ensure the canoe modle is facing the right direction.
        canoe.rotate([0.0, 0.5, 0.0], math.radians(90))
        canoe.rotate([0.5, 0.0, 0.0], math.radians(-1 * 90))

        print("Model Generated")
        # Create a new plot
        return canoe

    def Mesh_Generate(self):
        CI, CO = self.Coordinate_Generate("3D")

        Vectors_I = []
        Vectors_O = []
        # Convert the coordinate format in to vectors formate. In which they are X,Y,Z (Width,Depth,Length)
        for num in range(0, self.Num):
            for c_set in CI[num]:
                MeshSet = []
                # For Debug
                """print("X:%s || Y:%s || Z:%s"%(c_set[0][0], c_set[1][0], c_set[2][0]))"""
                for x, y, z in zip(c_set[0], c_set[1], c_set[2]):
                    if (self.Log[2] == 24):
                        add = (self.Depth[num] + self.Thickness) - c_set[1][-1]
                        if (self.FSDMode):
                            MeshSet.append([x, y + add, z + self.Thickness])


                        elif ((self.CoverLength - self.Thickness) <= z <= (
                                sum(self.Length) - self.CoverLength - self.B2 + self.Thickness)):

                            MeshSet.append([x, y + add, z + self.Thickness])
                            """print(f"[{x},{y+add},{z+self.Thickness}]")"""
                    else:
                        # add is the value to add to the Y coordinate to make the top of canoe body start at same
                        # point (the depth of the canoe body).
                        add = (self.Depth[num] + self.Thickness) - c_set[1][-1]
                        if (self.FSDMode):
                            MeshSet.append([x, y + add, z + self.Thickness])

                        elif ((self.CoverLength - self.Thickness) <= z <= (
                                sum(self.Length) - self.CoverLength + self.Thickness)):

                            MeshSet.append([x, y + add, z + self.Thickness])
                            """print(f"[{x},{y+add},{z+self.Thickness}]")"""

                if (MeshSet != []):
                    Vectors_I.append(MeshSet)

            for c_set_o in CO[num]:
                MeshSet = []
                # For Debug
                """print("X_O:%s || Y_O:%s || Z_O:%s"%(c_set_o[0][0], c_set_o[1][0], c_set_o[2][0]))"""
                for x, y, z in zip(c_set_o[0], c_set_o[1], c_set_o[2]):
                    add = (self.Depth[num] + self.Thickness) - c_set_o[1][-1]
                    MeshSet.append([x, y + add, z])
                Vectors_O.append(MeshSet)
        return ([Vectors_I, Vectors_O])

    def Hall_Mesh_Generate(self, V_List):
        # The Hall_Mesh_Generate is for generating the mesh of the hall in a data structure that can be mathmatically convert in
        # to a STL formate.

        # The V_List is the list of the vertex of the hall.
        Face_List = []
        for number, V_set in enumerate(V_List):
            F_L = []
            if (number == 0):  # meaning is inside
                for C_Index in range(1, len(V_set)):
                    inner = V_set[C_Index - 1]
                    outer = V_set[C_Index]
                    Point4_Set = []

                    for P4 in range(1, len(inner)):
                        Point4_Set.append(
                            [inner[P4], inner[P4 - 1], outer[P4], outer[P4 - 1]])
                    F_L.append(Point4_Set)
            else:  # outside
                for C_Index in range(1, len(V_set)):
                    inner = V_set[C_Index - 1]
                    outer = V_set[C_Index]

                    Point4_Set = []

                    for P4 in range(1, len(inner)):
                        Point4_Set.append(
                            [inner[P4 - 1], inner[P4], outer[P4 - 1], outer[P4]])
                    F_L.append(Point4_Set)
            Face_List.append(F_L)
        return Face_List

    def Connection_Mesh_Generate(self, Vertex_I, Vertex_O):
        ConnectionMesh = []
        for index in range(1, len(Vertex_I)):
            ConnectionMesh.append([[Vertex_I[index][0], Vertex_I[index - 1][0],
                                    Vertex_O[index][0], Vertex_O[index - 1][0]]])
            ConnectionMesh.append([[Vertex_I[index - 1][1], Vertex_I[index][1],
                                    Vertex_O[index - 1][1], Vertex_O[index][1]]])
        return ConnectionMesh

    def Horizontal_Cover_Mesh_Generate(self, Vertext_Out_Set_Cover_List):
        Horizontal_Mesh_List = []
        for index, Vertex_Set_Cover in enumerate(Vertext_Out_Set_Cover_List):
            Vertex_Positive_List = []
            Vertex_Negative_List = []
            Horizontal_Mesh = []
            for Vertex_Set in Vertex_Set_Cover:
                """
                Data Structure of Vertex_Set: (example)
                [[-0.0, 14.75, 0.0], [0.0, 14.75, 0.0]]
                Consider the Section of self.Vertex_Generating
                """
                Vertex_Positive_List.append(Vertex_Set[-1])
                Vertex_Negative_List.append(Vertex_Set[0])

            for Vertex_Index in range(1, len(Vertex_Positive_List)):
                Horizontal_Mesh.append([Vertex_Positive_List[Vertex_Index], Vertex_Positive_List[Vertex_Index - 1],
                                        Vertex_Negative_List[Vertex_Index], Vertex_Negative_List[Vertex_Index - 1]])

            Horizontal_Mesh_List.append(Horizontal_Mesh)

        return Horizontal_Mesh_List

    def Vertical_Cover_Mesh_Generate(self, VerticalCoverList):
        # Vertical Cover Mesh Generation (Only for normal model that require cover, vertical cover.)

        FaceVertical = []
        Cset_Vertical_List = []
        for index, Cover_Vertical in enumerate(VerticalCoverList):
            VertexSet = []
            Cset_Vertical = []  # a curve
            Cset_Horizontal = []  # a "line"

            # assert coordinate sets
            for index_sub, coordinate_set in enumerate(Cover_Vertical):

                if (index_sub != 0 and 0 == index):
                    coordinate_set_copy = coordinate_set + []
                    coordinate_set_copy[1] = Cover_Vertical[0][1]  # same height as 0th element
                    Cset_Horizontal.append(coordinate_set_copy)
                elif (index_sub != len(Cover_Vertical) - 1 and index != 0):
                    coordinate_set_copy = coordinate_set + []
                    coordinate_set_copy[1] = Cover_Vertical[0][1]  # same height as the last element
                    Cset_Horizontal.append(coordinate_set_copy)
                Cset_Vertical.append(coordinate_set)
                Cset_Vertical_List.append(Cset_Vertical)

            # create faces
            if (index == 0):
                for C_index in range(1, len(Cset_Horizontal)):
                    VertexSet.append([Cset_Vertical[C_index - 1], Cset_Vertical[C_index],
                                      Cset_Horizontal[C_index - 1], Cset_Horizontal[C_index]])
            else:
                Cset_Horizontal.reverse()
                Cset_Vertical.reverse()
                for C_Index_sub in range(1, len(Cset_Horizontal)):
                    VertexSet.append([Cset_Vertical[C_Index_sub - 1], Cset_Vertical[C_Index_sub],
                                      Cset_Horizontal[C_Index_sub - 1], Cset_Horizontal[C_Index_sub]])

            FaceVertical.append(VertexSet)

        return FaceVertical, Cset_Vertical_List

    # To generate Graph of consecration per a specific interval.
    def Construction_Graph_Generation(self):
        if (self.Construction == False):
            return 42

        graph_list = []
        for Section_Index, section in enumerate(self.Coordinate_Construction):
            # cross_index == cross_section_index
            graph_section_list = []
            # construction graph interval setting
            Copy_Section = []

            # process to take off the cover
            for check in range(0, len(section)):
                if (section[check][2][-1] - int(section[check][2][-1]) == 0):
                    Copy_Section.append(section[check])

            for cross_index in range(0, len(Copy_Section), 4):
                if not (self.EWidthF[Section_Index] == 0 and self.EDepthF[Section_Index] == 0):
                    graph_section_list.append(
                        [Copy_Section[cross_index][0], Copy_Section[cross_index][1], Copy_Section[cross_index][-1]])
            if ([Copy_Section[-1][0], Copy_Section[-1][1], Copy_Section[-1][-1]] not in graph_section_list):
                graph_section_list.append([Copy_Section[-1][0], Copy_Section[-1][1], Copy_Section[-1][-1]])
            graph_list.append(graph_section_list)

        return graph_list

    # To generate all coordinate of the canoe.
    def Coordinate_Generate(self, ModeString):
        # The list that save the curve function for each 1 inch in length

        # This part can be simplified into a one by another function. TDB
        CurveList_Inside, CurveList_Outside = self.Formula_Generate()

        Coordinate_Inside: list[list[list[Union[list[Union[int, Any]], list[Any]]]]] = []
        Coordinate_Outside: list[list[list[Union[list[Union[int, Any]], list[Any]]]]] = []
        self.Coordinate_Construction: list[list[list[Union[list[Union[int, Any]], list[Any]]]]] = []

        # Structure of Coordinate list above would be:
        # Canoe[
        #   Section[
        #           CrossSection[
        #                        X[float,float...],
        #                        Y[float,float...],
        #                        Z[float,float...],
        #                        len(X) = len(Y) = len(Z)
        #                        ],
        #           CrossSection[],
        #           CrossSection[],
        #           ],
        #   Section[]..
        #       ]

        # Addition structure for Coordinate_Construction
        # Canoe[
        #   Section[
        #           CrossSection[
        #                        X[float,float...],
        #                        Y[float,float...],
        #                        Z[float,float...],
        #           difference-> infor[str: formula, int: inch, formulaCoefficient: set(Coefficient, Exponent)]
        #                        len(X) = len(Y) = len(Z)
        #                        ],
        #           CrossSection[],
        #           CrossSection[],
        #           ],
        #   Section[]..
        #       ]

        interval = 1

        count_in = 0
        count_out = 0

        for num in range(0, self.Num):
            CI_List, count_in = self.Coordinate_Section_Generate(
                num, count_in, self.Inside_LengthList, self.Inside_Length,
                CurveList_Inside, interval, ModeString)
            CO_List, count_out = self.Coordinate_Section_Generate(
                num, count_out, self.Outside_LengthList, self.Outside_Length,
                CurveList_Outside, interval, ModeString)

            Coordinate_Inside.append(CI_List)
            Coordinate_Outside.append(CO_List)

        if (self.Construction == True):
            count_construct = 0
            # male module for construction, thus use inner data.
            for num in range(0, self.Num):
                CU_List, count_construct = self.Coordinate_Section_Generate(
                    num, count_construct, self.Inside_LengthList, self.Inside_Length,
                    CurveList_Inside, interval, "Construction")
                self.Coordinate_Construction.append(CU_List)

        """# used to Debug of Construction
        for i in Coordinate_Construction:
            for j in i:
                print(f"formula: {j[-1][0]} at {j[-1][1]} inch")
                for x,y,z in zip(j[0],j[1],j[2]):
                    print(f"X: {x}, Y: {y}, Z: {z}")
                print("\n")
            print("\n\n\n")"""

        # Used to Debug
        """
        print("First Section")

        for i, j in zip(Coordinate_Inside[0], CurveList_Inside[0]):
            print("Inside Function: %s" % (j[0]))
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

    def Coordinate_Section_Generate(self, num, count, CalculateLengthList, ModelLengthList, CurveList, interval,
                                    ModeString):
        C_List = []
        # C_List = [CrossSection, CrossSection, CrossSection, ...]

        for dataIndex in range(len(CalculateLengthList[num])):
            if (num == 0):
                X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                    CurveList[num][dataIndex][1], interval, CurveList[num][dataIndex][0],
                    ModelLengthList[count], ModeString)
                C_List.append([X_List, Y_List, Z_List])
            else:
                # if the change rate of this section's width and depth both are 0.
                if (self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):

                    X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                        CurveList[num][0][1], interval, CurveList[num][0][0],
                        ModelLengthList[count], ModeString)  # length subtake
                    C_List.append([X_List, Y_List, Z_List])
                else:
                    if (self.Log[2] == 24):
                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList[num][dataIndex][1], interval, CurveList[num][dataIndex][0],
                            ModelLengthList[count], ModeString)
                        C_List.append([X_List, Y_List, Z_List])
                    else:
                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList[num][dataIndex][1], interval, CurveList[num][dataIndex][0],
                            ModelLengthList[count], ModeString)
                        C_List.append([X_List, Y_List, Z_List])
            # the extra actions that only for the condition when the user choose to generate construction graphs.
            if (ModeString == "Construction"):
                x = X_List[-1] ** self.ECurveF[num]
                y = Y_List[-1]
                z = Z_List[-1]
                Coefficient = y / x if x != 0 else 0
                formula = f"{round(Coefficient, 8)}x^{self.ECurveF[num]}" if x != 0 else 0
                C_List[-1].append([formula, z, (Coefficient, self.ECurveF[num])])
            count += 1

        return C_List, count

    def Formula_Generate(self):
        CurveFbyInch_Inside = []
        CurveFbyInch_Outside = []

        for num in range(self.Num):
            CL_In = []
            CL_Out = []

            if (self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):
                CL_In = [[self.BuildLambda_Curve_Constant(num), self.SemiWidth[num], self.Depth[num]]]
                CL_Out = [[self.BuildLambda_Curve_Constant_Out(num), (self.SemiWidth[num] + self.Thickness),
                           (self.Depth[num] + self.Thickness)]]

            elif (self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):

                for length in self.Inside_LengthList[num]:
                    if (type(self.DepthFList[num]) in [float, int]):
                        Depth = self.DepthFList[num]

                    else:
                        Depth = self.DepthFList[num](length)
                    Width = self.WidthFList[num](length)
                    if (Width == 0 or Depth == 0):
                        CL_In.append(
                            [self.Buildlambda_Curve_Zero(), Width, Depth])

                    else:
                        CL_In.append(
                            [self.BuildLambda_Curve(Width, Depth, num), Width, Depth])

                for length_out in self.Outside_LengthList[num]:

                    if (type(self.DepthFList_Outside[num]) in [float, int]):
                        Depth_O = self.DepthFList_Outside[num]

                    else:
                        Depth_O = self.DepthFList_Outside[num](length_out)
                    Width_O = self.WidthFList_Outside[num](length_out)
                    if (Width_O == 0 or Depth_O == 0):
                        CL_Out.append(
                            [self.Buildlambda_Curve_Zero(), Width_O, Depth_O])
                    else:
                        CL_Out.append(
                            [self.BuildLambda_Curve(Width_O, Depth_O, num), Width_O, Depth_O])

            CurveFbyInch_Inside.append(CL_In)
            CurveFbyInch_Outside.append(CL_Out)

        # reverse the end to make it pare with the canoe body
        CurveFbyInch_Inside[-1].reverse()
        # assert cover to the right length
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
        Vertex_O_Cover = [[], []]
        FrontCover = V_List[0][0][0][-1]
        EndCover = V_List[0][-1][0][-1]
        # Get Vectors for Inside and Outside
        for VI in V_List[0]:
            Vertex_I.append([VI[0], VI[-1]])
        for VO in V_List[1]:
            if (self.FSDMode):
                Vertex_O.append([VO[0], VO[-1]])

            else:
                if (FrontCover <= VO[0][-1] <= EndCover):
                    Vertex_O.append([VO[0], VO[-1]])
                if (VO[0][-1] <= FrontCover or VO[0][-1] >= EndCover):
                    if (VO[0][-1] <= FrontCover):
                        Vertex_O_Cover[0].append([VO[0], VO[-1]])
                    else:
                        Vertex_O_Cover[-1].append([VO[0], VO[-1]])

        return (Vertex_I, Vertex_O, Vertex_O_Cover)

    def CrossSection_Coordinate_Generate(self, width, interval, function, zvalue, ModeString):

        xlist = []
        ylist = []
        zlist = []

        if (ModeString == "3D"):
            # Find the largest Width, confirm the Width step interval
            Max_Width = max(self.Width)

            L_Width = Max_Width
            step_interval = width / L_Width

            for i in range(0, int(L_Width)):
                w = step_interval * i

                xlist.append(w)
                ylist.append(function(w))
                zlist.append(zvalue)

            # get the last one
            xlist.append(width)
            ylist.append(function(width))
            zlist.append(zvalue)


        elif (ModeString == "Construction"):
            # config the interval from 1 to 0.5 to get more accuracy.
            step_interval = 0.5
            step = width / step_interval

            for i in range(0, int(step) + 1):
                w = step_interval * i

                xlist.append(w)
                ylist.append(function(w))
                zlist.append(zvalue)


            # get the last one
            xlist.append(width)
            ylist.append(function(width))
            zlist.append(zvalue)

        nxlist = xlist[1:]

        for x, y in zip(nxlist, ylist[1:]):
            xlist.insert(0, x * -1)
            ylist.insert(0, y)
            zlist.append(zvalue)

        return (xlist, ylist, zlist)

    # To generate all z index along the canoe body.
    def LengthIndexGenerate(self):
        # 1.1
        # Inside_Length and Outside_Length are list, in which they contain the specific length index of each section of the canoe.
        # For example, if the canoe is 3 sections, and each section's length is 100, 200, 300.
        # Then the Inside_Length = [[0...100],[0...200],[0...300]], and for the Outside_Length, we need to add the thickness of the canoe body.
        # In which Outside_Length = [[0...100+Thickness],[0...200+Thickness],[0...300+Thickness]]

        # 1.2
        # Inside_LengthList and Outside_LengthList are list, in which they culmulatively calculate each length index along the canoe and store them.
        # For example, if the canoe is 3 sections, and each section's length is 100, 200, 300.
        # Then the Inside_LengthList = [[0...100],[100...300],[300...600]], and for the Outside_LengthList, we need to add the thickness of the canoe body.
        # In which Outside_LengthList = [[0...100+Thickness],[100+Thickness...300+Thickness],[300+Thickness...600+Thickness]]

        # 1.3
        # Since the canoe contain at least one cover, we need to find the index of the cover in either Length and LengthList.

        interval = 1
        print(self.Log)
        # Assign the length index of covers.
        if (self.Log[2] == 24):
            cover_list_in = [self.CoverLength - self.Thickness,
                             self.CoverLength_end - self.B2 + self.Thickness]
            cover_list_out = [self.CoverLength,
                              self.CoverLength_end - self.B2 + self.Thickness * 2]

            length = self.GetLengthList(self.Length, False, True)
            len_sum_out = self.GetLengthList(self.Length, True, True)
            len_sum_in = length
        else:
            cover_list_in = [self.CoverLength - self.Thickness,
                             self.CoverLength_end + self.Thickness]
            cover_list_out = [self.CoverLength,
                              self.CoverLength_end + self.Thickness * 2]

            len_sum_in = self.GetLengthList(self.Length, False, False)
            len_sum_out = self.GetLengthList(self.Length, True, False)

        CoverIndexList_in = []
        CoverIndexList_out = []
        # Find the index of the cover in the length list.
        for cover_in, cover_out in zip(cover_list_in, cover_list_out):
            numIn = ModelCalculation.LocateCover(cover_in, len_sum_in) - 1
            numOut = ModelCalculation.LocateCover(cover_out, len_sum_out) - 1
            if (numIn == self.Num - 1):  # mean the numIndex is the last
                CoverIndexList_in.append([numIn, abs(len_sum_in[numIn + 1] - float(cover_in))])
            else:
                CoverIndexList_in.append([numIn, abs(len_sum_in[numIn] - float(cover_in))])

            if (numOut == self.Num - 1):
                CoverIndexList_out.append([numOut, abs(len_sum_out[numIn + 1] - float(cover_out))])
            else:
                CoverIndexList_out.append([numOut, abs(len_sum_out[numIn] - float(cover_out))])

        # check if the point is already included
        for CoverIndex_in, CoverIndex_out in zip(CoverIndexList_in, CoverIndexList_out):
            if (math.isclose(CoverIndex_in[1], len_sum_in[CoverIndex_in[0]])):
                CoverIndexList_in.remove(CoverIndex_in)
            if (math.isclose(CoverIndex_out[1], len_sum_out[CoverIndex_out[0]])):
                CoverIndexList_out.remove(CoverIndex_out)

        for numIndex in range(self.Num):
            lenIn_list = []
            lenOut_list = []

            if (self.Num == 3 and numIndex == 1):
                if (self.Log[2] == 24):
                    for length_In in np.arange(self.B2, self.Length[numIndex], interval):
                        lenIn_list.append(length_In)
                        if (length_In + interval >= self.Length[numIndex]):
                            lenIn_list.append(self.Length[numIndex])
                            break
                    for length_Out in np.arange(self.B2_O, self.Length[numIndex] + self.B2_Diff, interval):
                        lenOut_list.append(length_Out)
                        if (length_Out + interval >= self.Length[numIndex] + self.B2_Diff):
                            lenOut_list.append(self.Length[numIndex] + self.B2_Diff)
                            break

                else:
                    for length_In in np.arange(0, self.Length[numIndex], interval):
                        lenIn_list.append(length_In)
                        if (length_In + interval >= self.Length[numIndex]):
                            lenIn_list.append(self.Length[numIndex])
                            break
                    for length_Out in np.arange(0, self.Length[numIndex], interval):
                        lenOut_list.append(length_Out)
                        if (length_Out + interval >= self.Length[numIndex]):
                            lenOut_list.append(self.Length[numIndex])
                            break


            else:
                for length_In in np.arange(0, self.Length[numIndex], interval):
                    lenIn_list.append(length_In)
                    if (length_In + interval >= self.Length[numIndex]):
                        lenIn_list.append(self.Length[numIndex])
                        break

                for length_Out in np.arange(0, self.Length[numIndex] + self.Thickness, interval):
                    lenOut_list.append(length_Out)
                    if (length_Out + interval >= self.Length[numIndex] + self.Thickness):
                        lenOut_list.append(self.Length[numIndex] + self.Thickness)
                        break

            # Avoid the length of assertion list of cover is no equal, so can't use zip()

            self.InsertCover(lenIn_list, CoverIndexList_in, self.B2, numIndex)
            self.InsertCover(lenOut_list, CoverIndexList_out, self.B2_O, numIndex)

            self.Inside_LengthList.append(lenIn_list)
            self.Outside_LengthList.append(lenOut_list)

        self.Inside_Length = self.ZIndexGenerate(copy.deepcopy(self.Inside_LengthList), len_sum_in, self.B2)
        self.Outside_Length = self.ZIndexGenerate(copy.deepcopy(self.Outside_LengthList), len_sum_out, self.B2_O)

    def InsertCover(self, lenlist, CoverIndexList, B2, numIndex):
        # Inser the cover into the length list.
        for CoverIndex in CoverIndexList:
            if (CoverIndex[0] == numIndex):
                if (CoverIndex[1] not in lenlist):
                    if (self.Log[2] == 24 and numIndex == 1):
                        lenlist.append(CoverIndex[1] + B2)
                        lenlist.sort()
                    else:
                        lenlist.append(CoverIndex[1])
                        lenlist.sort()

    def ZIndexGenerate(self, LengthList, LenSum, B2):
        if (self.Log[2] == 24):
            for index, element in enumerate(LengthList[1]):
                LengthList[1][index] = element - B2
        resultList = []
        for index in range(len(LengthList) - 1):
            for element in LengthList[index]:
                resultList.append(round(element + LenSum[index], 8))

        LengthList[-1].reverse()
        for element in LengthList[-1]:
            resultList.append(round(LenSum[-1] - element, 8))

        return resultList

    @staticmethod
    def LocateCover(canoe_cover, length_list):
        # This function is used to find the which section of canoe the cover is in.
        for lenIndex in range(1, len(length_list)):
            if (canoe_cover < length_list[lenIndex - 1] and lenIndex - 1 == 0):
                return lenIndex - 1
            elif (length_list[lenIndex - 1] < canoe_cover < length_list[lenIndex]):
                return lenIndex
            elif (math.isclose(length_list[lenIndex - 1], canoe_cover)):
                return lenIndex - 1
            elif (math.isclose(length_list[lenIndex], canoe_cover)):
                return lenIndex + 1

    def GetLengthList(self, lengthList, isOut=False, b2_indicate=False):
        # return the list of length with correct x coordinate
        # exp: lengthList[36,120,36]
        # function return [0,36,156,192]
        Sum = 0
        Len_Sum = [0]
        for index, length in enumerate(lengthList):
            Sum += length

            if (isOut):
                if (index == len(lengthList) - 1 or index == 0):
                    Sum += self.Thickness
            if (b2_indicate and index == 1):
                Sum -= self.B2

            Len_Sum.append(Sum)
        return Len_Sum

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
