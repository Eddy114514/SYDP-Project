import tkinter as tk
import numpy as np
from scipy.integrate import quad
from tkinter import messagebox
from PIL import Image, ImageTk
from sympy import *
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from stl import mesh
import math


class MainGUI_Base():
    def __init__(self, master):
        self.root = master
        self.root.geometry("800x800")
        self.root.title("Canoe Design Software")
        MainGUI_Init(self.root)


class MainGUI_Init():
    def __init__(self, master):
        self.master = master
        self.MainGUI_Init_MainFrame = tk.Frame(self.master)
        self.MainGUI_Init_MainFrame.pack()
        self.ConfigImg()
        self.CreateWidgets()

    def ConfigImg(self):
        img_CreatNew = Image.open('Picture\\CreatNew_Icon.png')
        img_CreatNew = img_CreatNew.resize((80, 100), Image.ANTIALIAS)
        self.img_resized_CreatNew = ImageTk.PhotoImage(img_CreatNew)

        img_Open = Image.open('Picture\\Open_Icon.png')
        img_Open = img_Open.resize((80, 100), Image.ANTIALIAS)
        self.img_resized_Open = ImageTk.PhotoImage(img_Open)

        img_Findbest = Image.open('Picture\\FindBest_icon.png')
        img_Findbest = img_Findbest.resize((80, 100), Image.ANTIALIAS)
        self.img_resized_Findbest = ImageTk.PhotoImage(img_Findbest)

        img_Return = Image.open('Picture\\Menu_Icon.png')
        img_Return = img_Return.resize((50, 50), Image.ANTIALIAS)
        MainGUI_Init.img_resized_Return = ImageTk.PhotoImage(img_Return)

        img_Add = Image.open('Picture\\Add_Icon.png')
        img_Add = img_Add.resize((50, 50), Image.ANTIALIAS)
        MainGUI_Init.img_resized_Add = ImageTk.PhotoImage(img_Add)

        img_NextPage = Image.open('Picture\\NextPage_Icon.png')
        img_NextPage = img_NextPage.resize((50, 50), Image.ANTIALIAS)
        MainGUI_Init.img_resized_NextPage = ImageTk.PhotoImage(img_NextPage)

        img_BackPage = Image.open('Picture\\BackPage_Icon.png')
        img_BackPage = img_BackPage.resize((50, 50), Image.ANTIALIAS)
        MainGUI_Init.img_resized_BackPage = ImageTk.PhotoImage(img_BackPage)

        img_Save = Image.open('Picture\\Save_Icon.png')
        img_Save = img_Save.resize((50, 50), Image.ANTIALIAS)
        MainGUI_Init.img_resized_Save = ImageTk.PhotoImage(img_Save)

    def CreateWidgets(self):

        username_label = tk.Label(self.MainGUI_Init_MainFrame, text="Canoe Design Program", font=(
            "Time", 15, "bold")).pack(pady=10)

        CreatNew_Button = tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_CreatNew, text="New Project", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwitch_CreatNew).pack(pady=40)

        Open_Button = tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_Open, text="Open Project", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwitch_Open).pack(pady=40)

        CreatNew_Button = tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_Findbest, text="Design Optimization", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwicth_FindBest).pack(pady=0)

    def PgSwitch_CreatNew(self):
        self.MainGUI_Init_MainFrame.destroy()
        MainGUI_CreatNEW(self.master)

    def PgSwitch_Open(self):
        self.MainGUI_Init_MainFrame.destroy()
        MainGUI_CreatNEW(self.master)

    def PgSwicth_FindBest(self):
        self.MainGUI_Init_MainFrame.destroy()
        MainGUI_CreatNEW(self.master)


class MainGUI_CreatNEW():

    Num_Counter = 0
    Page_Counter = 0

    def __init__(self, master):
        self.master = master
        self.creatWidgets_PageMain()
        self.creatWidgets_PageOne(True)
        self.creatWidgets_PageTwo(False)
        self.creatWidgets_PageThree(False)

        self.PageStoreList = [self.creatWidgets_PageOne,
                              self.creatWidgets_PageTwo, self.creatWidgets_PageThree]

        self.FrameStoreList = [[self.MainGUI_InputTable, self.Return_Button], [
            self.MainGUI_InputTable_Two, self.BackPage_Button], [self.MainGUI_DisplayTable_Three, self.BackPage_Button, self.Save_Button]]

    def creatWidgets_PageMain(self):

        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue")
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master, bg="green")
        self.MainGUI_Title.pack(fill="x", pady=50)

        username_label = tk.Label(self.MainGUI_Title, text="Data Input Table", font=(
            "Time", 15, "bold")).pack(pady=10)

        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage, command=lambda: [self.SaveData(MainGUI_CreatNEW.Num_Counter, MainGUI_CreatNEW.Page_Counter), self.NextPage()])
        self.NextPage_Button.pack(side="right", padx=10, pady=10)

    def creatWidgets_PageOne(self, SON, STR="Null"):

        if(SON == False):
            self.MainGUI_InputTable = 0
            self.Return_Button = 0

        if(SON == True):

            SectionDictObject = {}
            HullDictObject = []
            self.CDD = CanoeDataBase(SectionDictObject, HullDictObject)

            print("IN The Page One")
            MainGUI_CreatNEW.Num_Counter = 0
            self.MainGUI_InputTable = tk.Frame(self.master)
            self.MainGUI_InputTable.columnconfigure(0, weight=3)
            self.MainGUI_InputTable.columnconfigure(1, weight=3)
            self.MainGUI_InputTable.columnconfigure(2, weight=3)
            self.MainGUI_InputTable.columnconfigure(4, weight=3)
            self.MainGUI_InputTable.columnconfigure(5, weight=3)
            self.MainGUI_InputTable.columnconfigure(6, weight=3)
            self.MainGUI_InputTable.pack(fill="x", pady=150)
            self.DataInputTable(0)
            self.Return_Button = tk.Button(
                self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Return, command=self.Return)
            self.Return_Button.pack(side="left", padx=10, pady=10)

            if(STR == "Update"):
                self.FrameStoreList[0][0] = self.MainGUI_InputTable
                self.FrameStoreList[0][1] = self.Return_Button

    def creatWidgets_PageTwo(self, SON, STR="Null"):

        if(SON == False):
            self.MainGUI_InputTable_Two = 0
            self.BackPage_Button = 0

        if(SON == True):
            print("IN The Page TWO")
            self.MainGUI_InputTable_Two = tk.Frame(self.master)
            self.MainGUI_InputTable_Two.columnconfigure(0, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(1, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(2, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(4, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(5, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(6, weight=3)
            self.MainGUI_InputTable_Two.pack(fill="x", pady=150)
            self.DataInputTable_PageTWO()
            self.BackPage_Button = tk.Button(self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_BackPage, command=lambda: [
                                            self.PreviousPage_One()])
            self.BackPage_Button.pack(side="left", padx=10, pady=10)
            if(STR == "Update"):
                self.FrameStoreList[1][0] = self.MainGUI_InputTable_Two
                self.FrameStoreList[1][1] = self.BackPage_Button

    def creatWidgets_PageThree(self, SON, STR="Null"):
        if(SON == False):
            self.MainGUI_DisplayTable_Three = 0
            self.BackPage_Button = 0
            self.Save_Button = 0
        if(SON == True):
            self.CCO = Calculation(self.CDD)

            self.MainGUI_DisplayTable_Three = tk.Frame(self.master)
            self.MainGUI_DisplayTable_Three.columnconfigure(0, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(1, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(2, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(4, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(5, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(6, weight=3)
            self.MainGUI_DisplayTable_Three.pack(fill="x", pady=150)

            self.NextPage_Button.destroy()

            self.BackPage_Button = tk.Button(self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_BackPage, command=lambda: [
                                            self.PreviousPage_Two()])
            self.BackPage_Button.pack(side="left", padx=10, pady=10)

            self.Save_Button = tk.Button(
                self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Save, command=lambda: [self.CDD.SaveDataIntoFile()])
            self.Save_Button.pack(side="right", padx=10, pady=10)

            self.DisplayTable_PageThree()

            if(STR == "Update"):
                self.FrameStoreList[2][0] = self.MainGUI_DisplayTable_Three
                self.FrameStoreList[2][1] = self.BackPage_Button
                self.FrameStoreList[2][2] = self.Save_Button

    def DataInputTable(self, NumCount):
        #Defind Input table

        Length_entry_1 = tk.Entry(self.MainGUI_InputTable)
        Width_entry_1 = tk.Entry(self.MainGUI_InputTable)
        Depth_entry_1 = tk.Entry(self.MainGUI_InputTable)
        ExponentCurve_entry_1 = tk.Entry(self.MainGUI_InputTable)
        ExponentWidth_entry_1 = tk.Entry(self.MainGUI_InputTable)
        ExponentDepth_entry_1 = tk.Entry(self.MainGUI_InputTable)

        Length_entry_2 = tk.Entry(self.MainGUI_InputTable)
        Width_entry_2 = tk.Entry(self.MainGUI_InputTable)
        Depth_entry_2 = tk.Entry(self.MainGUI_InputTable)
        ExponentCurve_entry_2 = tk.Entry(self.MainGUI_InputTable)
        ExponentWidth_entry_2 = tk.Entry(self.MainGUI_InputTable)
        ExponentDepth_entry_2 = tk.Entry(self.MainGUI_InputTable)

        Length_entry_3 = tk.Entry(self.MainGUI_InputTable)
        Width_entry_3 = tk.Entry(self.MainGUI_InputTable)
        Depth_entry_3 = tk.Entry(self.MainGUI_InputTable)
        ExponentCurve_entry_3 = tk.Entry(self.MainGUI_InputTable)
        ExponentWidth_entry_3 = tk.Entry(self.MainGUI_InputTable)
        ExponentDepth_entry_3 = tk.Entry(self.MainGUI_InputTable)

        self.EntryDict = {0: [Length_entry_1, Width_entry_1, Depth_entry_1,
                              ExponentCurve_entry_1, ExponentWidth_entry_1,
                              ExponentDepth_entry_1],
                          1: [Length_entry_2, Width_entry_2, Depth_entry_2,
                              ExponentCurve_entry_2, ExponentWidth_entry_2,
                              ExponentDepth_entry_2],
                          2: [Length_entry_3, Width_entry_3, Depth_entry_3,
                              ExponentCurve_entry_3, ExponentWidth_entry_3,
                              ExponentDepth_entry_3]}

        SectionTitle_Label = tk.Label(self.MainGUI_InputTable,
                                      text="Section %s" % (int(
                                          NumCount/2)+1),
                                      font=("Time", 15)).grid(column=NumCount,
                                                              row=1,
                                                              sticky=tk.E,
                                                              ipady=5, ipadx=5)

        Length_label = tk.Label(self.MainGUI_InputTable,
                                text="Canoe Length :", font=(
                                    "Time", 12)).grid(column=NumCount, row=2,
                                                      sticky=tk.E, ipady=5,
                                                      ipadx=5)
        Width_label = tk.Label(self.MainGUI_InputTable,
                               text="Canoe Width :", font=(
                                   "Time", 12)).grid(column=NumCount, row=3,
                                                     sticky=tk.E, ipady=5,
                                                     ipadx=5)
        Depth_label = tk.Label(self.MainGUI_InputTable,
                               text="Canoe Depth :", font=(
                                   "Time", 12)).grid(column=NumCount, row=4,
                                                     sticky=tk.E, ipady=5,
                                                     ipadx=5)
        ExponentCurve_label = tk.Label(self.MainGUI_InputTable,
                                       text="Exponent of Curve function :",
                                       font=(
                                           "Time", 12)).grid(column=NumCount,
                                                             row=5, sticky=tk.E,
                                                             ipadx=5, ipady=5)
        ExponentWidth_label = tk.Label(self.MainGUI_InputTable,
                                       text="Exponent of Width function :",
                                       font=(
                                           "Time", 12)).grid(column=NumCount,
                                                             row=6, sticky=tk.E,
                                                             ipadx=5, ipady=5)
        ExponentDepth_label = tk.Label(self.MainGUI_InputTable,
                                       text="Exponent of Depth function :",
                                       font=(
                                           "Time", 12)).grid(column=NumCount,
                                                             row=7, sticky=tk.E,
                                                             ipadx=5, ipady=5)

        self.EntryDict[NumCount
                       / 2][0].grid(column=NumCount+1, row=2, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][1].grid(column=NumCount+1, row=3, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][2].grid(column=NumCount+1, row=4, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][3].grid(column=NumCount+1, row=5, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][4].grid(column=NumCount+1, row=6, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][5].grid(column=NumCount+1, row=7, sticky=tk.W)

        self.AddNewTable_Button = tk.Button(
            self.MainGUI_InputTable, image=MainGUI_Init.img_resized_Add, command=lambda: [self.Addtable(True, NumCount)])
        self.AddNewTable_Button.grid(
            column=NumCount+2, row=2, sticky=tk.W, padx=10)

        if(NumCount == 4):
            print("work5")
            self.Symmetry_CheckButton = tk.Checkbutton(
                self.MainGUI_InputTable, command=lambda: [self.CDD.ConfigSYM()], text="Symmetricity: ", font=(
                    "Time", 12))
            self.Symmetry_CheckButton.grid(
                column=NumCount+2, row=1, sticky=tk.W, padx=10)

    def DataInputTable_PageTWO(self):
        self.CoverLength_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.Density_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.Thickness_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.CrewWeight_entry = tk.Entry(self.MainGUI_InputTable_Two)

        CoverLenth_label = tk.Label(self.MainGUI_InputTable_Two, text="Cover Length :", font=(
            "Time", 12)).grid(column=0, row=1, sticky=tk.E, ipady=5, ipadx=5)
        Density_label = tk.Label(self.MainGUI_InputTable_Two, text="Concret Density :", font=(
            "Time", 12)).grid(column=0, row=2, sticky=tk.E, ipady=5, ipadx=5)
        Thickness = tk.Label(self.MainGUI_InputTable_Two, text="Concret Thickness :", font=(
            "Time", 12)).grid(column=0, row=3, sticky=tk.E, ipady=5, ipadx=5)
        CrewWeight_label = tk.Label(self.MainGUI_InputTable_Two, text="CrewWeight :", font=(
            "Time", 12)).grid(column=0, row=4, sticky=tk.E, ipadx=5, ipady=5)

        self.CoverLength_entry.grid(column=1, row=1, sticky=tk.W)
        self.Density_entry.grid(column=1, row=2, sticky=tk.W)
        self.Thickness_entry.grid(column=1, row=3, sticky=tk.W)
        self.CrewWeight_entry.grid(column=1, row=4, sticky=tk.W)

    def DisplayTable_PageThree(self):
        Label = tk.Label(self.MainGUI_DisplayTable_Three, text="Works", font=(
            "Time", 12)).grid(column=0, row=1, sticky=tk.E, ipady=5, ipadx=5)

        self.CCO.CalDataReturn()
        self.CCO.Model_Generate()

    def Addtable(self, booleanTable=0, NumCount=0):
        if(booleanTable and NumCount < 4):

            self.SaveData(NumCount/2, MainGUI_CreatNEW.Page_Counter)
            NumCount += 2
            self.AddNewTable_Button.destroy()
            self.DataInputTable(NumCount)
            MainGUI_CreatNEW.Num_Counter = NumCount/2
            print(MainGUI_CreatNEW.Num_Counter)

        elif(booleanTable and NumCount == 4):
            self.SaveData(NumCount/2, MainGUI_CreatNEW.Page_Counter)
            self.AddNewTable_Button.destroy()
            print(MainGUI_CreatNEW.Num_Counter)
            messagebox.showinfo("information", "Reach The MAX Section Number")

    def SaveData(self, Numcount, Pagenum):

        print(Numcount, "Num is ")

        if(Numcount <= 2 and Pagenum == 0):
            print("Enter First Dict", Numcount)
            Length_Canoe = float(self.EntryDict[Numcount][0].get())
            Width_Canoe = float(self.EntryDict[Numcount][1].get())
            Depth_Canoe = float(self.EntryDict[Numcount][2].get())
            ExponentCurve_Canoe = float(self.EntryDict[Numcount][3].get())
            ExponentWidth_Canoe = float(self.EntryDict[Numcount][4].get())
            ExponentDepth_Canoe = float(self.EntryDict[Numcount][5].get())

            SectionDataList = [Length_Canoe, Width_Canoe, Depth_Canoe,
                               ExponentCurve_Canoe, ExponentWidth_Canoe, ExponentDepth_Canoe]

            self.CDD.ConstructDict_SDD(Numcount, SectionDataList)

        elif(Pagenum > 0):
            print("Enter SEC Dict", Numcount)
            CoverLength = float(self.CoverLength_entry.get())
            Concret_Density = float(self.Density_entry.get())
            Concret_Thickness = float(self.Thickness_entry.get())
            CrewWeight = float(self.CrewWeight_entry.get())

            HullDataList = [CoverLength, Concret_Density,
                            Concret_Thickness, CrewWeight]

            self.CDD.ConstructDict_HDD(HullDataList)

            print(self.CDD)

    def Return(self):
        self.CDD.DeletData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.MainGUI_InputTable.destroy()
        MainGUI_Init(self.master)

    def NextPage(self):
        MainGUI_CreatNEW.Num_Counter += 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter+1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")

    def PreviousPage_One(self):
        self.CDD.DeletData_SDD()
        MainGUI_CreatNEW.Num_Counter -= 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter-1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")

    def PreviousPage_Two(self):
        self.CDD.DeletData_HDD()
        MainGUI_CreatNEW.Num_Counter -= 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter-1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")
        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage, command=lambda: [self.SaveData(MainGUI_CreatNEW.Num_Counter, MainGUI_CreatNEW.Page_Counter), self.NextPage()])
        self.NextPage_Button.pack(side="right", padx=10, pady=10)


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
                         22: "Assign HullType -> Symmetric Constant Hull", 23: "Assign HullType -> Asymmetric Constant Hull",
                         24: "Assign HullType -> Asymmetric Hull"}

        self.SignData()

    def SignData(self):
        SDD, HDD = self.CalculationObject.GetData_CDD()

        for v in SDD.values():
            self.Length.append(v[0])
            self.Width.append(v[1])
            self.SemiWidth.append(v[1]/2)
            self.Depth.append(v[2])
            self.ECurveF.append(v[3])
            self.EWidthF.append(v[4])
            self.EDepthF.append(v[5])

        self.CoverLength = HDD[0]
        self.Density = HDD[1]
        self.Thickness = HDD[2]
        self.CrewWeight = HDD[3]

        print(self.Length)
        print(self.Width)
        print(self.SemiWidth)
        print(self.Depth)

        print(self.ECurveF)
        print(self.EWidthF)
        print(self.EDepthF)

        print(self.CoverLength)
        print(self.Density)
        print(self.Thickness)
        print(self.CrewWeight)

        self.Num = len(self.Length)

        print(self.Num)

        self.SignFunction_Main()

    def CalDataReturn(self):
        if(self.SymmetryBoolean == True):
            self.Note.insert(1, 10)
        elif(self.SymmetryBoolean == False):
            self.Note.insert(1, 11)
        # Print the OperationNote
        for num in self.Note:
            print(self.NoteMenu[num])

    def SignFunction_Main(self):

        if(len(self.ECurveF) == 1):
            self.Note.append(0)
            self.SignFunction_SymmetryHull()

        elif(len(self.ECurveF) == 2):
            self.Note.append(1)
            self.SignFunction_TwoBodyHull()

        elif(len(self.ECurveF) == 3):
            self.Note.append(2)
            self.SignFunction_ThreeBodyHull()

    def BuildLambad_Width(self, index):
        return (lambda x: self.SemiWidth[index]*(x/self.Length[index])**self.EWidthF[index])

    def BuildLambad_Depth(self, index):
        return(lambda x: self.Depth[index]*(x/self.Length[index])**self.EDepthF[index])

    def BuildLambad_Width_O(self, index):
        return(lambda x: (
            self.SemiWidth[index]+self.Thickness)*(x/(self.Length[index]+self.Thickness))**self.EWidthF[index])

    def BuildLambad_Depth_O(self, index):
        return(lambda x: (self.Depth[index]+self.Thickness)*(x/(self.Length[index]+self.Thickness))**self.EDepthF[index])

    def BuildLambad_Width_Semi(self):
        SemiLength = self.Length[0]/2
        return(lambda x: self.SemiWidth[0]*(x/SemiLength)**self.EWidthF[0])

    def BuildLambad_Depth_Semi(self):
        SemiLength = self.Length[0]/2
        return(lambda x: self.Depth[0]*(x/SemiLength)**self.EDepthF[0])

    def BuildLambad_Width_Semi_O(self):
        SemiLength = self.Length[0]/2
        return(lambda x: (
            self.SemiWidth[0]+self.Thickness)*(x/(SemiLength+self.Thickness))**self.EWidthF[0])

    def BuildLambad_Depth_Semi_O(self):
        SemiLength = self.Length[0]/2
        return(lambda x: (
            self.Depth[0]+self.Thickness)*(x/(SemiLength+self.Thickness))**self.EDepthF[0])

    def SignFunction_SymmetryHull(self):
        self.Note.append(20)

        self.SymmetryBoolean = True

        self.WidthFList.append(self.BuildLambad_Width_Semi()
                               )
        self.WidthFList_Outside.append(self.BuildLambad_Width_Semi_O())
        self.DepthFList.append(self.BuildLambad_Depth_Semi()
                               )
        self.DepthFList_Outside.append(self.BuildLambad_Depth_Semi_O())

    def SignFunction_TwoBodyHull(self):

        if(self.Length[0] == self.Length[1] and self.SemiWidth[0] == self.SemiWidth[1] and self.Depth[0] == self.Depth[1] and self.EWidthF[0] == self.EWidthF[1] and self.EDepthF[0] == self.EDepthF[1]):
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

        if(self.Length[0] == self.Length[2] and self.SemiWidth[0] == self.SemiWidth[2] and self.Depth[0] == self.Depth[2] and self.EWidthF[0] == self.EWidthF[2] and self.EDepthF[0] == self.EDepthF[2]):
            self.SymmetryBoolean = True

        if(self.SymmetryBoolean):
            self.SignFunction_ThreeBodyHull_Constant(self.SymmetryBoolean)

        elif(self.SymmetryBoolean == False):
            if(self.EWidthF[1] == 0 and self.EDepthF[1] == 0):
                self.SignFunction_ThreeBodyHull_Constant(self.SymmetryBoolean)
            elif(self.EWidthF[1] != 0 and self.EDepthF[1] != 0):
                self.SignFunction_ThreeBodyHUll_Asymmetric()

    def SignFunction_ThreeBodyHull_Constant(self, SBoolean):
        if(SBoolean == True):
            self.Note.append(22)
        elif(SBoolean == False):
            self.Note.append(23)

        for index in range(0, len(self.EDepthF)):
            if(self.EWidthF[index] != 0 and self.EDepthF[index] != 0):
                self.WidthFList.append(self.BuildLambad_Width(index))
                self.WidthFList_Outside.append(self.BuildLambad_Width_O(index))
                self.DepthFList.append(self.BuildLambad_Depth(index)
                                       )
                self.DepthFList_Outside.append(self.BuildLambad_Depth_O(index)
                                               )
            elif(self.EWidthF[index] == 0 and self.EDepthF[index] == 0):
                self.WidthFList.append(-1)
                self.WidthFList_Outside.append(-1)
                self.DepthFList.append(-1)
                self.DepthFList_Outside.append(-1)

    def SignFunction_ThreeBodyHUll_Asymmetric(self):
        self.Note.append(24)
        # Sign Function for Front
        self.WidthFList.append(
            self.BuildLambad_Width(0))
        self.WidthFList_Outside.append(
            self.BuildLambad_Width_O(0))
        self.DepthFList.append(self.BuildLambad_Depth(0)
                               )
        self.DepthFList_Outside.append(self.BuildLambad_Depth_O(0))
        # Confirm Cross-sectional data for Middle Section

    def Concret_Volume(self):

        SwDFunction_List = []
        SwD_Out_Function_List = []
        Volume_Inside_List = []
        Volume_Outside_List = []
        Volume_Inside = 0
        Volume_Outside = 0

        if(self.Note[2] != 24):
            for k in range(0, len(self.WidthFList)):
                if(self.WidthFList[k] == -1 and self.DepthFList[k] == -1 and self.WidthFList_Outside[k] == -1 and self.DepthFList_Outside[k] == -1):
                    SwDFunction_List.append(lambda x: (
                        ((self.SemiWidth[k]**self.ECurveF[k])*x)/(self.Depth[k]))**(1/self.ECurveF[k]))
                    SwD_Out_Function_List.append(lambda x: (
                        (((self.SemiWidth[k]+self.Thickness)**self.ECurveF[k])*x)/(self.Depth[k]+self.Thickness))**(1/self.ECurveF[k]))

                elif(self.WidthFList[k] != -1 and self.DepthFList[k] != -1 and self.WidthFList_Outside[k] != -1 and self.DepthFList_Outside[k] != -1):
                    SwDFunction_List.append(lambda x: (
                        self.WidthFList[k](x)*self.DepthFList[k](x)))
                    SwD_Out_Function_List.append(lambda x: (
                        self.WidthFList_Outside[k](x)*self.DepthFList_Outside[k](x)))

            if(len(self.WidthFList) == -1 and len(self.DepthFList) == -1):

                Volume_Inside_List.append(2*2
                                          * ((self.ECurveF[0])/(self.ECurveF[0]+1))
                                          * quad(SwDFunction_List[0], 0, self.Length[0]/2)[0])
                Volume_Outside_List.append(2*2
                                           * ((self.ECurveF[0])/(self.ECurveF[0]+1))
                                           * quad(SwD_Out_Function_List[0], 0, self.Length[0]/2+self.Thickness)[0])

            elif(len(self.WidthFList) != -1 and len(self.DepthFList) != -1):
                for index in range(0, len(self.WidthFList)):
                    if(self.WidthFList[index] == -1 and self.DepthFList[index] == -1):
                        Volume_Inside_List.append(
                            self.Length[index]*2*quad(SwDFunction_List[index], 0, self.Depth[index])[0])
                        Volume_Outside_List.append(
                            self.Length[index]*2*quad(SwD_Out_Function_List[index], 0, (self.Depth[index]+self.Thickness))[0])
                    elif(self.WidthFList[index] != -1 and self.DepthFList[index] != -1):
                        Volume_Inside_List.append(
                            2*((self.ECurveF[index])/(self.ECurveF[index]+1))*quad(SwDFunction_List[index], 0, self.Length[index])[0])
                        Volume_Outside_List.append(2*((self.ECurveF[index])/(self.ECurveF[index]+1))*quad(
                            SwD_Out_Function_List[index], 0, self.Length[index]+self.Thickness)[0])
        elif(self.Note[2] == 24):
            print("fuck")

        for i, j in zip(Volume_Inside_List, Volume_Outside_List):
            Volume_Inside += i
            Volume_Outside += j
        print(Volume_Inside)
        print(Volume_Outside)

    def Styrofoam_Volume():
        print("k")

    def Model_Generate(self):
        if(len(self.Length) == 1):
            self.Symmetriclize()

        interval = 1

        V_List = self.Mesh_Generate()

        Vertex_I, Vertex_O, LenList = self.Vertex_Generating(V_List)
        CoverList = [self.CoverLength+self.Thickness,
                     sum(self.Length)-self.CoverLength+self.Thickness*2]

        formatSave = []
        Index_Set = []

        for FLBL in CoverList:
            Set_Index = self.PairCoverLength(LenList, FLBL)
            formula, W = self.Single_Formula_Generate(
                self.CoverLength, Set_Index[1])

            X, Y, Z = self.CrossSection_Coordinate_Generate(
                W, interval, formula, FLBL, "3D")

            if(LenList[Set_Index[0]] != FLBL):
                Format = self.XYZ_Format_Generating(X, Y, Z, Set_Index[1])
                formatSave.append(Format)
                if(FLBL == CoverList[0]):
                    V_List[0].insert(Set_Index[0], Format)
                elif(FLBL == CoverList[-1]):
                    V_List[0].insert(Set_Index[0]+1, Format)

        if(len(V_List[0]) < len(V_List[1])):
            V_List = self.Add_To_Equal(V_List)

        for format in formatSave:
            Index_Set.append(V_List[0].index(format))

        Face_List = []
        Face_Num = 0

        for V_set in V_List:
            F_L = []
            for add in range(len(V_set[1])-1):
                V_set[0].append(V_set[0][0])
                V_set[-1].append(V_set[-1][0])
            for C_Index in range(1, len(V_set)):
                inner = V_set[C_Index-1]
                outter = V_set[C_Index]

                Point4_Set = []
                for P4 in range(1, len(inner)):
                    Point4_Set.append(
                        [inner[P4-1], inner[P4], outter[P4-1], outter[P4]])
                F_L.append(Point4_Set)
            Face_List.append(F_L)

        Inter, Cover, Cover_H = self.Vertical_Horizontal_Mesh_Generate(
            V_List, Index_Set)
        Face_List.append(Inter)
        Face_List.append(Cover)
        Face_List.append(Cover_H)

        for l in Face_List:
            for p in l:
                Face_Num += len(p)*2

        # Sign Front and Back

        cube = mesh.Mesh(np.zeros(Face_Num, dtype=mesh.Mesh.dtype))

        #Resigning the Coordinate

        face_Counter = 0
        for list in Face_List:
            for face in list:
                for set in face:
                    #Sign Two faces
                    for num in range(3):
                        cube.vectors[face_Counter][num] = set[num]
                        cube.vectors[face_Counter+1][num] = set[num+1]
                    face_Counter += 2
        cube.rotate([0.0, 1, 0.0], math.radians(90))
        cube.rotate([1, 0.0, 0.0], math.radians(-1*90))

        cube.save('cube.stl')

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

    def Add_To_Equal(self, V_List):
        for add in range(len(V_List[1])-len(V_List[0]), 2):
            print("Add for Two")
            V_List[0].append(V_List[0][-1])
            V_List[0].insert(V_List[0][0])

        return (V_List)

    def XYZ_Format_Generating(self, X, Y, Z, num):

        Formate = []
        for x, y, z in zip(X, Y, Z):
            add = (self.Depth[num]+self.Thickness) - Y[-1]
            Formate.append([x, y+add, z])

        return(Formate)

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

        return(Vertex_I, Vertex_O, Length_List)

    def PairCoverLength(self, LenList, find):
        NearbyList = []
        Diff = math.inf
        NearbyList = []

        Sum = 0
        Len_Sum = [0]
        for length in self.Length:
            Sum += length
            Len_Sum.append(Sum)

        for Index, Compare in enumerate(LenList):

            if(int(Compare) == int(find)):
                NearbyList.append([Compare, Index])

        ReturnSet = []
        for Len, Target in enumerate(NearbyList):

            if(find >= Target[0]):

                if(Len == len(NearbyList)-1):
                    print("Find|%s| > Target[0]|%s|, at Index|%s|" % (
                        find, Target[0], Len))
                    ReturnSet.append(Target[1]+1)
            elif(find < Target[0]):

                if(Len == 0):
                    print("Find|%s| < Target[0]|%s|, at Index|%s|" % (
                        find, Target[0], Len))
                    ReturnSet.append(Target[1])

        for num in range(1, len(Len_Sum)):
            if(find > Len_Sum[num-1] and find <= Len_Sum[num]):
                ReturnSet.append(num-1)
        print(ReturnSet)
        return(ReturnSet)

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

        for index in range(1, len(Vertex_I)):
            F_L.append([[Vertex_I[index-1][0], Vertex_I[index][0],
                         Vertex_O[index-1][0], Vertex_O[index][0]]])
            F_L.append([[Vertex_I[index-1][1], Vertex_I[index][1],
                         Vertex_O[index-1][1], Vertex_O[index][1]]])

        for set in Vertex_I:
            LP.append(set[1])
            LN.append(set[0])

        for index in range(1, IndexSet[0]):
            print([[LP[index-1], LP[index], LN[index-1], LN[index]]])
            F_L1.append([[LP[index-1], LP[index], LN[index-1], LN[index]]])

        for index in range(IndexSet[1]+1, len(LP)):
            F_L1.append([[LP[index-1], LP[index], LN[index-1], LN[index]]])

        IndexSet[1] = IndexSet[1]-1
        for I in IndexSet:
            CN = []
            CP = []
            print("\n")
            for Coordinate in V_List[0][I]:
                if(Coordinate[0] <= 0.0):
                    CN.append(Coordinate)
                if(Coordinate[0] >= 0.0):
                    CP.append(Coordinate)
            CP.reverse()
            Set = []
            for Index in range(1, len(CP)):
                print([[CP[Index-1], CP[Index], CN[Index-1], CN[Index]]])
                Set.append([CP[Index-1], CP[Index], CN[Index-1], CN[Index]])
            F_L2.append(Set)

        return(F_L, F_L1, F_L2)

    def Single_Formula_Generate(self, ZLength, num):
        SymX = Symbol('x')

        print(num)
        F1 = self.WidthFList[num]
        F2 = self.DepthFList[num]

        if(F1 == -1):
            def F1(x): return self.SemiWidth[num]

        if(F2 == -1):
            def F2(x): return self.Depth[num]

        Width = F1(ZLength)
        Depth = F2(ZLength)

        return (Depth*(SymX/Width)**self.ECurveF[num], Width)

    def Mesh_Generate(self):
        CI, CO = self.Coordinatie_Generate("3D")

        Vectors_I = []
        Vectors_O = []

        for num in range(0, self.Num):
            for c_set in CI[num]:
                Set = []
                for x, y, z in zip(c_set[0], c_set[1], c_set[2]):
                    add = (self.Depth[num]+self.Thickness) - c_set[1][-1]
                    Set.append([x, y+add, z+self.Thickness])
                Vectors_I.append(Set)

            for c_set_o in CO[num]:
                Set = []
                for x, y, z in zip(c_set_o[0], c_set_o[1], c_set_o[2]):
                    add = (self.Depth[num]+self.Thickness) - c_set_o[1][-1]
                    Set.append([x, y+add, z])
                Vectors_O.append(Set)
        return ([Vectors_I, Vectors_O])

    def Coordinatie_Generate(self, ModeString):
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
                if(self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):
                    Z_value -= interval
                    for L_index in np.arange(0, self.Length[num], interval):

                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(

                            CurveList_Inside[num][dataIndex][1], interval, CurveList_Inside[num][dataIndex][0], Z_value, ModeString)
                        CI_List.append([X_List, Y_List, Z_List])
                        if(L_index + interval >= self.Length[num]):
                            X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                CurveList_Inside[num][dataIndex][1], interval, CurveList_Inside[num][dataIndex][0], Z_value+interval, ModeString)
                            CI_List.append([X_List, Y_List, Z_List])
                        Z_value += interval

                    if(L_index + interval >= self.Length[num]):
                        Z_value -= interval

                elif(self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):
                    if(CurveList_Inside[num][dataIndex][0] == 0):
                        CI_List.append([[0], [0], [Z_value]])

                    elif(CurveList_Inside[num][dataIndex][0] != 0):

                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList_Inside[num][dataIndex][1], interval, CurveList_Inside[num][dataIndex][0], Z_value, ModeString)
                        CI_List.append([X_List, Y_List, Z_List])
                Z_value += interval

            for dataIndex_O in range(0, len(CurveList_Outside[num])):
                if(self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):
                    Z_value_O -= interval
                    for L_Index_O in np.arange(0, self.Length[num], interval):
                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0], Z_value_O, ModeString)
                        CO_List.append([X_List, Y_List, Z_List])
                        if(L_Index_O + interval >= self.Length[num]):
                            X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0], Z_value_O+interval, ModeString)
                            CO_List.append([X_List, Y_List, Z_List])

                        Z_value_O += interval
                        if(L_Index_O + interval >= self.Length[num]):
                            Z_value_O -= interval

                elif(self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):

                    if((dataIndex_O == len(CurveList_Outside[num])-1 and num == 0) or (dataIndex_O == 0 and num == len(self.Length)-1)):

                        if(num == 0 and dataIndex_O == len(CurveList_Outside[num])-1):
                            Z_value_O += self.Thickness-interval
                            if(CurveList_Outside[num][dataIndex_O][0] != 0):
                                X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                    CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0], Z_value_O, ModeString)
                                CO_List.append([X_List, Y_List, Z_List])
                        elif(num == len(self.Length)-1 and dataIndex_O == 0):

                            if(CurveList_Outside[num][dataIndex_O][0] != 0):
                                X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                                    CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0], Z_value_O, ModeString)
                                CO_List.append([X_List, Y_List, Z_List])
                                Z_value_O += self.Thickness-interval

                    elif(CurveList_Outside[num][dataIndex_O][0] != 0 and dataIndex_O+interval < len(CurveList_Outside[num])):
                        X_List, Y_List, Z_List = self.CrossSection_Coordinate_Generate(
                            CurveList_Outside[num][dataIndex_O][1], interval, CurveList_Outside[num][dataIndex_O][0], Z_value_O, ModeString)
                        CO_List.append([X_List, Y_List, Z_List])

                    elif(CurveList_Outside[num][dataIndex_O][0] == 0):
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

    def CrossSection_Coordinate_Generate(self, width, interval, function, zvalue, ModeString):

        xlist = []
        ylist = []
        zlist = []
        nxlist = []

        SymX = Symbol('x')

        if(ModeString == "3D"):
            # Find the largest Width, confirm the Width step interval
            Max_Width = 0

            for W in self.SemiWidth:
                if(W > Max_Width):
                    Max_Width = W

            L_Width = Max_Width
            step_interval = width/L_Width

            for i in range(0, int(L_Width)+1):
                w = step_interval * i

                xlist.append(w)
                ylist.append(function.subs(SymX, w))
                zlist.append(zvalue)

                if(w < width and (i+1)*step_interval > width and int(L_Width) < Max_Width):

                    xlist.append(width)
                    ylist.append(function.subs(SymX, width))
                    zlist.append(zvalue)

        elif(ModeString == "Construction"):
            for i in np.arange(0, width, interval):

                xlist.append(i)
                ylist.append(function.subs(SymX, i))
                zlist.append(zvalue)

                if(i + interval >= width):
                    xlist.append(width)
                    ylist.append(function.subs(SymX, width))
                    zlist.append(zvalue)

        nxlist = xlist[1:]

        for x, y in zip(nxlist, ylist[1:]):
            xlist.insert(0, x*-1)
            ylist.insert(0, y)
            zlist.append(zvalue)

        return (xlist, ylist, zlist)

    def Formula_Generate(self):
        CurveFbyInch_Inside = []
        CurveFbyInch_Outside = []
        SymX = Symbol('x')
        interval = 1
        for num in range(self.Num):
            CL_In = []
            CL_Out = []

            if(self.EWidthF[num] == 0.0 and self.EDepthF[num] == 0.0):
                CL_In = [[self.Depth[num]*(SymX/self.SemiWidth[num])
                          ** self.ECurveF[num], self.SemiWidth[num], self.Depth[num]]]
                CL_Out = [[(self.Depth[num]+self.Thickness)*(SymX/(self.SemiWidth[num]+self.Thickness))
                           ** self.ECurveF[num], (self.SemiWidth[num]+self.Thickness), (self.Depth[num]+self.Thickness)]]

            elif(self.EWidthF[num] != 0.0 and self.EDepthF[num] != 0.0):

                for length in np.arange(0, self.Length[num], interval):
                    Width = self.WidthFList[num](length)
                    Depth = self.DepthFList[num](length)

                    CL_In.append(
                        [Depth*(SymX/Width)**self.ECurveF[num], Width, Depth])
                    if(length + interval >= self.Length[num]):
                        Width = self.WidthFList[num](self.Length[num])
                        Depth = self.DepthFList[num](self.Length[num])
                        CL_In.append(
                            [Depth*(SymX/Width)**self.ECurveF[num], Width, Depth])

                for length_out in np.arange(0, self.Length[num]+self.Thickness, interval):
                    Width_O = self.WidthFList_Outside[num](length_out)
                    Depth_O = self.DepthFList_Outside[num](length_out)

                    CL_Out.append(
                        [Depth_O*(SymX/Width_O)**self.ECurveF[num], Width_O, Depth_O])

                    if(length_out + interval >= self.Length[num]+self.Thickness):
                        Width_O = self.WidthFList_Outside[num](
                            self.Length[num]+self.Thickness)
                        Depth_O = self.DepthFList_Outside[num](
                            self.Length[num]+self.Thickness)
                        CL_Out.append(
                            [Depth_O*(SymX/Width_O)**self.ECurveF[num], Width_O, Depth_O])
            CurveFbyInch_Inside.append(CL_In)
            CurveFbyInch_Outside.append(CL_Out)

        # reverse the end to make it pare with the canoe body
        CurveFbyInch_Inside[-1].reverse()
        CurveFbyInch_Outside[-1].reverse()

        return(CurveFbyInch_Inside, CurveFbyInch_Outside)

    def Symmetriclize(self):
        self.Num += 1
        self.Length.append(self.Length[0]/2)
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

        print(self.WidthFList)
        print(self.WidthFList_Outside)
        print(self.DepthFList)
        print(self.DepthFList_Outside)


class CanoeDataBase():

    def __init__(self, SectionDataDict, HullDataDict):
        self.SDD = SectionDataDict
        self.HDD = HullDataDict
        self.SymmetryBoolean = False

    def ConfigSYM(self):
        print("Change from ", self.SymmetryBoolean)
        if(self.SymmetryBoolean):
            self.SymmetryBoolean = False
        elif(self.SymmetryBoolean == False):
            self.SymmetryBoolean = True
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

    def SaveDataIntoFile(self):
        #Save Data
        print("work")


if __name__ == "__main__":
    root = tk.Tk()

    MainGUI_Base(root)
    root.mainloop()
