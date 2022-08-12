from tkinter import filedialog

from matplotlib import pyplot
from mpl_toolkits import mplot3d

import Messagebox112 as messagebox
import Tkinter_112 as tk
# Import other files
from HealthCheck import *
from OptimizationCalculation import OptimizationCalculation


# change to 112 graphic
# Done

# learned how to use "with open", "eval" from
# https://www.w3schools.com/python/python_file_open.asp
# https://www.geeksforgeeks.org/with-statement-in-python/
# https://www.programiz.com/python-programming/methods/built-in/eval


class MainGUI_Base():
    # read startUp file
    if (platform.system().lower() == 'windows'):
        SetUpinformation = '..\\..\\asset\\startSetup\\setUpinformation.txt'
    else:
        SetUpinformation = '././asset/startSetup/setUpinformation.txt'

    with open(SetUpinformation) as dict:
        startSetUp = dict.read()
    dB = DebugBase(bool(eval(startSetUp)['isDebug']))  # isDebug Parameter

    def __init__(self, master):

        self.HC = HealthCheckBase('Main_GUI')

        if (MainGUI_Base.dB.isDebug == True):
            sys.stderr.flush()  # refresh
            print("""keyword explain:
            1. sym : mean test a symmetric hall 
            2. lsh  : mean test a LongShort Hull
            3. sch : mean test a Symmetric Constant Hull
            4. ach : mean test a Asymmetric Constant Hull
            5. ath  : mean test a Asymmetric Hull
            """)
            self.Profile = input("Enter the TestProfile: ")
            MainGUI_Base.dB.DebugMode(self.Profile)
        else:
            self.root = master
            self.root.geometry = "800*800"
            self.root.title = "Canoe Design Software"
            MainGUI_Init(self.root)


class MainGUI_Init():

    def __init__(self, master):
        self.master = master
        self.MainGUI_Init_MainFrame = tk.Frame(self.master, height=master.geometry[0], width=master.geometry[1])
        self.MainGUI_Init_MainFrame.pack()
        self.ConfigImg()
        self.CreateWidgets()

    def ConfigImg(self):
        if(platform.system().lower() == "windows"):
            # https://www.iconfinder.com/icons/802066/add_create_document_new_new_document_plus_create_document_icon
            self.img_resized_CreatNew = '../../asset/Picture/CreatNew_Icon.png'

            # http://megane2.ru/load/url=http:/www.perspectivy.info/photography/open-file-icon-png.html
            self.img_resized_Open = '../../asset/Picture/Open_Icon.png'

            # https://thenounproject.com/icon/optimisation-2754529/
            self.img_resized_Findbest = '../../asset/Picture/FindBest_Icon.png'

            # https://icon-library.com/icon/icon-menu-png-10.html configure manully

            MainGUI_Init.img_resized_Return = '../../asset/Picture/Menu_Icon.png'

            # https://www.flaticon.com/free-icon-font/add_3914248

            MainGUI_Init.img_resized_Add = '../../asset/Picture/Add_Icon.png'

            # https://italian.cri.cn/zt/xinjiang/index.html

            MainGUI_Init.img_resized_NextPage = '../../asset/Picture/NextPage_Icon.png'

            # https://italian.cri.cn/zt/xinjiang/index.html just a manually reverse
            MainGUI_Init.img_resized_BackPage = '../../asset/Picture/BackPage_Icon.png'

            # https://www.pngfind.com/mpng/iiiRibm_png-file-save-icon-vector-png-transparent-png/
            MainGUI_Init.img_resized_Save = '../../asset/Picture/Save_Icon.png'
        else:
            self.img_resized_CreatNew = '././asset/Picture/CreatNew_Icon.png'
            self.img_resized_Open = '././asset/Picture/Open_Icon.png'
            self.img_resized_Findbest = '././asset/Picture/FindBest_Icon.png'
            MainGUI_Init.img_resized_Return = '././asset/Picture/Menu_Icon.png'
            MainGUI_Init.img_resized_Add = '././asset/Picture/Add_Icon.png'
            MainGUI_Init.img_resized_NextPage = '././asset/Picture/NextPage_Icon.png'
            MainGUI_Init.img_resized_BackPage = '././asset/Picture/BackPage_Icon.png'
            MainGUI_Init.img_resized_Save = '././asset/Picture/Save_Icon.png'


    def CreateWidgets(self):
        # username_label
        FrameMaster = self.MainGUI_Init_MainFrame
        w = FrameMaster.width
        h = FrameMaster.height
        tk.Label(FrameMaster, text="Canoe Design Program", font=(
            "Time", 15, "bold")).pack(pady=10)

        # CreatNew_Button
        tk.Button(FrameMaster, width=w / 3, height=h / 5, image=self.img_resized_CreatNew, text="New Project", font=(
            "Time", 15, "bold"), command=self.PgSwitch_CreatNew).pack(pady=40)

        # Open_Button
        tk.Button(FrameMaster, width=w / 3, height=h / 5, image=self.img_resized_Open, text="Open Project", font=(
            "Time", 15, "bold"), command=self.PgSwitch_Open).pack(pady=40)

        # CreatNew_Button
        tk.Button(FrameMaster, width=w / 3, height=h / 5, image=self.img_resized_Findbest, text="Design Optimization",
                  font=(
                      "Time", 15, "bold"), command=self.PgSwitch_FindBest).pack(pady=20)

        # Debug Button
        self.Debug_Button = tk.Button(
            self.MainGUI_Init_MainFrame, text="Debug",
            command=lambda: [MainGUI_Base.dB.ChangDebug(True), sys.exit()])
        self.Debug_Button.pack(padx=10, pady=10)

    def PgSwitch_CreatNew(self):
        self.MainGUI_Init_MainFrame.destroy()
        MainGUI_CreatNEW(self.master)

    def PgSwitch_Open(self):

        InputFile_Path = self.GetFilePath()

        if (InputFile_Path != ""):
            self.MainGUI_Init_MainFrame.destroy()
            MainGUI_Open(self.master, InputFile_Path)

    def PgSwitch_FindBest(self):
        InputFile_Path = self.GetFilePath()

        if (InputFile_Path != ""):
            self.MainGUI_Init_MainFrame.destroy()
            MainGUI_Optimization(self.master, InputFile_Path)

    def GetFilePath(self):
        AbsFilePath = __file__
        AbsFilePath = AbsFilePath[0:AbsFilePath.index("Code")]
        if (platform.system().lower() == 'windows'):
            AbsFilePath += "asset\\__designHistory"
        else:
            AbsFilePath += "asset/__designHistory"
        try:
            InputFile_Path = filedialog.askopenfilename(title="Open Your Previous Design",
                                                        filetypes=[('Text file', '.txt')],
                                                        initialdir=AbsFilePath)
            return InputFile_Path
        except:
            messagebox.showMessage("Wrong Input")
            return ""


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
            self.MainGUI_InputTable_Two, self.BackPage_Button],
                               [self.MainGUI_DisplayTable_Three, self.BackPage_Button, self.Save_Button]]

    def creatWidgets_PageMain(self):

        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue", height=70)
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master, height=70)
        self.MainGUI_Title.pack(fill="x", pady=10)
        self.username_label = tk.Label(self.MainGUI_Title, text="", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=30)

        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, bg="gray", image=MainGUI_Init.img_resized_NextPage, width=60,
            height=self.MainGUI_Menu_Button.height - 10,
            command=lambda: [self.SaveData(MainGUI_CreatNEW.Num_Counter, MainGUI_CreatNEW.Page_Counter),
                             self.NextPage()])
        self.NextPage_Button.pack(anchor="e", padx=10, pady=5)

    # SON is PageConditionBoolean
    # STR is PageConditionKeyword
    def creatWidgets_PageOne(self, SON, STR="Null"):

        if (SON == False):
            self.MainGUI_InputTable = None
            self.Return_Button = 0

        if (SON == True):
            MainGUI_CreatNEW.Num_Counter = 0

            SectionDictObject = {}
            HullListObject = []
            self.CDD = CanoeDataBase(SectionDictObject, HullListObject)
            self.MainGUI_Title.configure(bg="green")
            self.username_label.configure(text="Data Input Table (1)")

            print("IN The Page One")
            MainGUI_CreatNEW.Num_Counter = 0
            self.MainGUI_InputTable = tk.Frame(self.master, width=500, height=500)
            self.MainGUI_InputTable.pack(fill="x", pady=10)
            self.MainGUI_InputTable.columnconfigure(12, 7)
            self.DataInputTable(0)
            self.Return_Button = tk.Button(
                self.MainGUI_Menu_Button, bg="gray", height=70, width=60, image=MainGUI_Init.img_resized_Return,
                command=self.Return)
            self.Return_Button.pack(anchor="w", padx=10, pady=5)

            if (STR == "Update"):
                self.FrameStoreList[0][0] = self.MainGUI_InputTable
                self.FrameStoreList[0][1] = self.Return_Button

    def creatWidgets_PageTwo(self, SON, STR="Null"):

        if (SON == False):
            self.MainGUI_InputTable_Two = None
            self.BackPage_Button = 0

        if (SON == True):
            self.MainGUI_Title.configure(bg="green")
            self.username_label.configure(text="Data Input Table (2)")
            print("IN The Page TWO")
            self.MainGUI_InputTable_Two = tk.Frame(self.master, height=500, width=self.master.geometry[0])
            self.MainGUI_InputTable_Two.columnconfigure(6, 6)
            self.MainGUI_InputTable_Two.pack(pady=150)
            self.DataInputTable_PageTWO()
            self.BackPage_Button = tk.Button(self.MainGUI_Menu_Button,bg = "gray", image=MainGUI_Init.img_resized_BackPage,
                                             command=lambda: [
                                                 self.PreviousPage_One()], height=70, width=60)
            self.BackPage_Button.pack(anchor="w", padx=10, pady=5)
            if (STR == "Update"):
                self.FrameStoreList[1][0] = self.MainGUI_InputTable_Two
                self.FrameStoreList[1][1] = self.BackPage_Button

    def creatWidgets_PageThree(self, SON, STR="Null"):
        if (SON == False):
            self.MainGUI_DisplayTable_Three = None
            self.BackPage_Button = 0
            self.Save_Button = 0
        if (SON == True):
            self.MainGUI_Title.configure(bg="red")
            self.username_label.configure(text="Result Table")

            self.MainGUI_DisplayTable_Three = tk.Frame(self.master, height=500, width=self.master.geometry[0])
            self.MainGUI_DisplayTable_Three.columnconfigure(6, 6)
            self.MainGUI_DisplayTable_Three.pack(pady=50)

            self.NextPage_Button.destroy()

            self.BackPage_Button = tk.Button(self.MainGUI_Menu_Button,bg = "gray", image=MainGUI_Init.img_resized_BackPage,
                                             command=lambda: [
                                                 self.PreviousPage_Two()], height=70, width=60, )
            self.BackPage_Button.pack(anchor="w", padx=10, pady=5)

            self.Save_Button = tk.Button(
                self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Save,
                command=lambda: [self.FileAcquire()], height=70, width=60)  # Acquire File and call CanoeDateBase
            self.Save_Button.pack(anchor="e", padx=10, pady=5)

            self.DisplayTable_PageThree()

            if (STR == "Update"):
                self.FrameStoreList[2][0] = self.MainGUI_DisplayTable_Three
                self.FrameStoreList[2][1] = self.BackPage_Button
                self.FrameStoreList[2][2] = self.Save_Button

    def DataInputTable(self, NumCount):
        # Defind Input table

        Length_entry_1 = tk.Entry(self.MainGUI_InputTable, width=40)
        Width_entry_1 = tk.Entry(self.MainGUI_InputTable, width=40)
        Depth_entry_1 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentCurve_entry_1 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentWidth_entry_1 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentDepth_entry_1 = tk.Entry(self.MainGUI_InputTable, width=40)

        Length_entry_2 = tk.Entry(self.MainGUI_InputTable, width=40)
        Width_entry_2 = tk.Entry(self.MainGUI_InputTable, width=40)
        Depth_entry_2 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentCurve_entry_2 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentWidth_entry_2 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentDepth_entry_2 = tk.Entry(self.MainGUI_InputTable, width=40)

        Length_entry_3 = tk.Entry(self.MainGUI_InputTable, width=40)
        Width_entry_3 = tk.Entry(self.MainGUI_InputTable, width=40)
        Depth_entry_3 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentCurve_entry_3 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentWidth_entry_3 = tk.Entry(self.MainGUI_InputTable, width=40)
        ExponentDepth_entry_3 = tk.Entry(self.MainGUI_InputTable, width=40)

        self.EntryDict = {0: [Length_entry_1, Width_entry_1, Depth_entry_1,
                              ExponentCurve_entry_1, ExponentWidth_entry_1,
                              ExponentDepth_entry_1],
                          1: [Length_entry_2, Width_entry_2, Depth_entry_2,
                              ExponentCurve_entry_2, ExponentWidth_entry_2,
                              ExponentDepth_entry_2],
                          2: [Length_entry_3, Width_entry_3, Depth_entry_3,
                              ExponentCurve_entry_3, ExponentWidth_entry_3,
                              ExponentDepth_entry_3]}

        LabelCount = NumCount if NumCount == 0 else NumCount + 0.5

        SectionTitle_Label = tk.Label(self.MainGUI_InputTable,
                                      text="Section %s" % (int(
                                          NumCount / 2) + 1),
                                      font=("Time", 15, "bold")).grid(column=LabelCount,
                                                                      row=1)

        Length_label = tk.Label(self.MainGUI_InputTable,
                                text="Canoe Length :", font=(
                "Time", 12, "")).grid(column=LabelCount, row=2)
        Width_label = tk.Label(self.MainGUI_InputTable,
                               text="Canoe Width :", font=(
                "Time", 12, "")).grid(column=LabelCount, row=3)
        Depth_label = tk.Label(self.MainGUI_InputTable,
                               text="Canoe Depth :", font=(
                "Time", 12, "")).grid(column=LabelCount, row=4)
        ExponentCurve_label = tk.Label(self.MainGUI_InputTable,
                                       text="Curve Exp:",
                                       font=(
                                           "Time", 12, "")).grid(column=LabelCount, row=5)
        ExponentWidth_label = tk.Label(self.MainGUI_InputTable,
                                       text="Width Exp:",
                                       font=(
                                           "Time", 12, "")).grid(column=LabelCount, row=6)
        ExponentDepth_label = tk.Label(self.MainGUI_InputTable,
                                       text="Depth Exp:",
                                       font=(
                                           "Time", 12, "")).grid(column=LabelCount, row=7)

        self.EntryDict[NumCount
                       / 2][0].grid(column=NumCount + 2, row=2)
        self.EntryDict[NumCount
                       / 2][1].grid(column=NumCount + 2, row=3)
        self.EntryDict[NumCount
                       / 2][2].grid(column=NumCount + 2, row=4)
        self.EntryDict[NumCount
                       / 2][3].grid(column=NumCount + 2, row=5)
        self.EntryDict[NumCount
                       / 2][4].grid(column=NumCount + 2, row=6)
        self.EntryDict[NumCount
                       / 2][5].grid(column=NumCount + 2, row=7)

        self.AddNewTable_Button = tk.Button(
            self.MainGUI_InputTable, image=MainGUI_Init.img_resized_Add, width=50, height=50,
            command=lambda: [self.Addtable(True, NumCount)])
        self.AddNewTable_Button.grid(
            column=NumCount + 2.5, row=2)

    def DataInputTable_PageTWO(self):
        self.CoverLength_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.Density_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.Thickness_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.CrewWeight_entry = tk.Entry(self.MainGUI_InputTable_Two)

        # CoverLenth_Label
        tk.Label(self.MainGUI_InputTable_Two, text="Cover Length :", font=(
            "Time", 12, "")).grid(column=0, row=1)
        # Density_Label
        tk.Label(self.MainGUI_InputTable_Two, text="Concrete Density :", font=(
            "Time", 12, "")).grid(column=0, row=2)
        # Thickness_Label
        tk.Label(self.MainGUI_InputTable_Two, text="Concrete Thickness :", font=(
            "Time", 12, "")).grid(column=0, row=3)
        # CrewWeight_Label
        tk.Label(self.MainGUI_InputTable_Two, text="CrewWeight :", font=(
            "Time", 12, "")).grid(column=0, row=4)

        self.CoverLength_entry.grid(column=1, row=1)
        self.Density_entry.grid(column=1, row=2)
        self.Thickness_entry.grid(column=1, row=3)
        self.CrewWeight_entry.grid(column=1, row=4)

    # learned how to embed 3d matplotlib into the Tkinter interface from line:
    #  https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
    def DisplayTable_PageThree(self):

        # Action
        try:
            self.DCCO = DataCalculation(self.CDD)  # DataCalculationCanoeObject
            self.MCCO = ModelCalculation(self.CDD)  # ModelCalculationCanoeObject
            self.DCCO.CanoeDataCalculation()
            # Print out Current Data
            self.logInt, self.CanoeData, self.OperationNote = self.DCCO.CalDataReturn()

            # Canoe Hall type defined
            tk.Label(self.MainGUI_DisplayTable_Three,
                     text=f"{self.OperationNote[0]} || {self.OperationNote[1]} || {self.OperationNote[2]}", font=(
                    "Time", 12, "")).grid(column=0, row=0)

            # Output display
            VolumeString = f"Canoe Volume :{round(self.CanoeData[1]['Volume'], 2)} cubic inch"
            WeightSrting = f"Canoe Weight :{round(self.CanoeData[1]['Weight'], 2)} lbs"
            BuoyancyString = f"Canoe Buoyancy :{round(self.CanoeData[1]['Buoyancy'], 2)} N"
            FlowString = f"Flow Test :{'Pass!' if self.CanoeData[1]['Flow'] else 'Not Pass!'}"
            Submerge = f"Submerge Test: {'Pass!' if self.CanoeData[1]['Submerge'] else 'Not Pass!'}"

            tk.Label(self.MainGUI_DisplayTable_Three, text=VolumeString, font=(
                "Time", 12, "bold")).grid(column=0, row=1)
            tk.Label(self.MainGUI_DisplayTable_Three, text=WeightSrting, font=(
                "Time", 12, "bold")).grid(column=0, row=2)
            tk.Label(self.MainGUI_DisplayTable_Three, text=BuoyancyString, font=(
                "Time", 12, "bold")).grid(column=0, row=3)
            tk.Label(self.MainGUI_DisplayTable_Three, text=FlowString, font=(
                "Time", 12, "bold")).grid(column=0, row=4)
            tk.Label(self.MainGUI_DisplayTable_Three, text=Submerge, font=(
                "Time", 12, "bold")).grid(column=0, row=5)

            # Model related
            self.canoe_mesh_object = self.MCCO.Model_Generate()
            # Generate the canoe
            # consider the example from https://pypi.org/project/numpy-stl/
            window = pyplot.figure()
            canvas = pyplot.subplot(projection="3d")
            # render
            canvas.add_collection3d(mplot3d.art3d.Poly3DCollection(self.canoe_mesh_object.vectors))

            scale = self.canoe_mesh_object.points.flatten()
            canvas.auto_scale_xyz(scale, scale, scale)

            pyplot.show()


        except:
            messagebox.showMessage("Wrong Data Input")
            self.MainGUI_DisplayTable_Three.destroy()
            self.CDD.DeleteData_CDD()
            self.MainGUI_Menu_Button.destroy()
            self.MainGUI_Title.destroy()
            MainGUI_Init(self.master)

    def Addtable(self, booleanTable=0, NumCount=0):
        if (booleanTable and NumCount < 4):

            continueBoolean = self.SaveData(NumCount / 2, MainGUI_CreatNEW.Page_Counter)
            if (continueBoolean):
                NumCount += 2
                self.AddNewTable_Button.destroy()
                self.DataInputTable(NumCount)
                MainGUI_CreatNEW.Num_Counter = NumCount / 2
                print(MainGUI_CreatNEW.Num_Counter)


        elif (booleanTable and NumCount == 4):
            self.SaveData(NumCount / 2, MainGUI_CreatNEW.Page_Counter)
            self.AddNewTable_Button.destroy()
            print(MainGUI_CreatNEW.Num_Counter)
            messagebox.showMessage("Reach The MAX Section Number")

    def FileAcquire(self):

        Folderpath = filedialog.askdirectory(title="Save STL Model")
        if (Folderpath == ""):  # no save when no input
            return 0
        # Directly Save Design
        self.CDD.SaveDataIntoFile(self.OperationNote, self.CanoeData, self.logInt)
        # Save the Model position by asking

        filename = self.OperationNote[-1].split("-> ")[-1] + "_Canoe.stl"
        filePath = f"{Folderpath}/{filename}"
        print(f"Model Save @ {Folderpath}/{filename}")
        self.CDD.SaveStlIntoFile(filePath, self.canoe_mesh_object)

    def SaveData(self, Numcount, PageNum):

        print(Numcount, "Num is ")

        if (Numcount <= 2 and PageNum == 0):
            print("Enter First Dict", Numcount)
            try:
                Length_Canoe = float(self.EntryDict[Numcount][0].get())
                Width_Canoe = float(self.EntryDict[Numcount][1].get())
                Depth_Canoe = float(self.EntryDict[Numcount][2].get())
                ExponentCurve_Canoe = float(self.EntryDict[Numcount][3].get())
                ExponentWidth_Canoe = float(self.EntryDict[Numcount][4].get())
                ExponentDepth_Canoe = float(self.EntryDict[Numcount][5].get())

                SectionDataList = [Length_Canoe, Width_Canoe, Depth_Canoe,
                                   ExponentCurve_Canoe, ExponentWidth_Canoe, ExponentDepth_Canoe]

                self.CDD.ConstructDict_SDD(Numcount, SectionDataList)
                return True
            except:
                messagebox.showMessage("Wrong input")



        elif (PageNum > 0):
            print("Enter SEC Dict", Numcount)
            CoverLength = float(self.CoverLength_entry.get())
            Concrete_Density = float(self.Density_entry.get())
            Concrete_Thickness = float(self.Thickness_entry.get())
            CrewWeight = float(self.CrewWeight_entry.get())

            HullDataList = [CoverLength, Concrete_Density,
                            Concrete_Thickness, CrewWeight]

            self.CDD.ConstructDict_HDL(HullDataList)

            print(self.CDD)

    def Return(self):
        self.CDD.DeleteData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.MainGUI_InputTable.destroy()
        MainGUI_Init(self.master)

    def NextPage(self):
        MainGUI_CreatNEW.Num_Counter += 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter + 1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")

    def PreviousPage_One(self):
        self.CDD.DeleteData_SDD()
        MainGUI_CreatNEW.Num_Counter -= 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter - 1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")

    def PreviousPage_Two(self):

        if (None in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]):
            # displayable 3 haven't finished
            messagebox.showMessage("Please Close The Model Window")
            return 0

        self.CDD.DeleteData_HDL()
        MainGUI_CreatNEW.Num_Counter -= 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter - 1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")
        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage,bg = "gray",
            command=lambda: [self.SaveData(MainGUI_CreatNEW.Num_Counter, MainGUI_CreatNEW.Page_Counter),
                             self.NextPage()], height=70, width=60, )
        self.NextPage_Button.pack(anchor="e", padx=10, pady=5)


class MainGUI_Open():
    def __init__(self, master, InputFilePath):
        self.master = master
        self.InputFile_Path = InputFilePath
        SectionDictObject = {}
        HullListObject = []
        self.CDD = CanoeDataBase(SectionDictObject, HullListObject)
        self.creatWidgets_PageMain()

    def creatWidgets_PageMain(self):
        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue", height=70)
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master, height=70)
        self.MainGUI_Title.pack(fill="x", pady=10)
        self.username_label = tk.Label(self.MainGUI_Title, text="", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=30)

        self.Return_Button = tk.Button(
            self.MainGUI_Menu_Button, bg="gray", height=70, width=60, image=MainGUI_Init.img_resized_Return,
            command=self.Return)
        self.Return_Button.pack(anchor="w", padx=10, pady=5)

        self.DisplayTable_PageMain()

    def DisplayTable_PageMain(self):
        self.MainGUI_Title.configure(bg="green")
        self.username_label.configure(text="Past Input")
        self.DisplayTable_PageMain_Frame = tk.Frame(self.master, height=500, width=self.master.geometry[0])

        with open(self.InputFile_Path, "r") as InputFile:
            self.InputFile = eval(InputFile.read())

        size = len(self.InputFile["Length"])
        self.DisplayTable_PageMain_Frame.columnconfigure((size * 3) + 1, 8, weight=1)
        self.DisplayTable_PageMain_Frame.pack(pady=50)

        # Store the Entry
        EntrySectionList = []
        # Store the UserLabel
        UserSectionLabel = []

        HallEntryList = self.AssignPreviousInput(size, EntrySectionList, UserSectionLabel)
        # CreateOtherPart
        for Col, (Entrylist, Labellist) in enumerate(zip(EntrySectionList, UserSectionLabel)):
            for Row, (Entry, Label) in enumerate(zip(Entrylist, Labellist)):
                Entry.grid(column=(Col * 3) + 1 + 0.5, row=Row + 1)
                Label.grid(column=(Col * 3) + 1 + 0.5, row=Row + 1)

        self.Next_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage,bg = "gray",
            command=lambda: [self.FileTransfer(EntrySectionList, HallEntryList)], height=70,
            width=60)  # Acquire File and call CanoeDateBase
        self.Next_Button.pack(anchor="e", padx=10, pady=5)

    def FileTransfer(self, EntryListSection, HallEntryList):
        SectionDictObject = {}
        HullListObject = []

        for sectionNum, Entrylist in enumerate(EntryListSection):
            SectionDictObject[sectionNum] = []
            for element in Entrylist:
                SectionDictObject[sectionNum].append(float(element.get()))

        for element in HallEntryList:
            HullListObject.append(float(element.get()))

        self.CDD = CanoeDataBase(SectionDictObject, HullListObject)
        try:
            self.DCCO = DataCalculation(self.CDD)
            self.MCCO = ModelCalculation(self.CDD)
            self.ResultTableDisplay()
        except:
            messagebox.showMessage("Wrong Config")
            self.DisplayTable_PageMain_Frame.destroy()
            self.Next_Button.destroy()
            self.DisplayTable_PageMain()

    def FileConfig(self):
        # Save the model at first
        Folderpath = filedialog.askdirectory(title="Save STL Model")
        filename = self.OperationNote[-1].split("-> ")[-1] + "_Canoe.stl"
        if (Folderpath != ""):
            filePath = f"{Folderpath}/{filename}"
            print(f"Model Save @ {Folderpath}/{filename}")
            self.CDD.SaveStlIntoFile(filePath, self.canoe_mesh_object)

        FileName = self.InputFile["Name"]
        if (platform.system().lower() == 'windows'):
            FileAddress =f"..\\..\\asset\\progressSave\\{'Design_' + FileName}"
        else:
            FileAddress = f"././asset/progressSave/{'Design_' + FileName}"

        self.CDD.WriteDataIntoFile(FileAddress, self.InputFile_Path, self.CanoeData, self.InputFile['Name'])

    def ResultTableDisplay(self):
        self.DisplayTable_PageMain_Frame.destroyAllElement()
        self.Next_Button.destroy()

        # GUI construct

        self.Save_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Save,
            command=lambda: [self.FileConfig(), self.Return()], height=70,
            width=60)
        self.Save_Button.pack(anchor="e", padx=10, pady=5)

        self.MainGUI_Title.configure(bg="red")
        self.username_label.configure(text="Result Display")

        try:
            self.DCCO.CanoeDataCalculation()
            self.canoe_mesh_object = self.MCCO.Model_Generate()
            # Print out Current Data
            self.logInt, self.CanoeData, self.OperationNote = self.DCCO.CalDataReturn()

            # Canoe Hall type defined
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text=f"{self.OperationNote[0]} || {self.OperationNote[1]} || {self.OperationNote[2]}", font=(
                    "Time", 12, "")).grid(column=0, row=0)

            # Output display
            VolumeString = f"Canoe Volume :{round(self.CanoeData[1]['Volume'], 2)} cubic inch"
            WeightSrting = f"Canoe Weight :{round(self.CanoeData[1]['Weight'], 2)} lbs"
            BuoyancyString = f"Canoe Buoyancy :{round(self.CanoeData[1]['Buoyancy'], 2)} N"
            FlowString = f"Flow Test :{'Pass!' if self.CanoeData[1]['Flow'] else 'Not Pass!'}"
            Submerge = f"Submerge Test: {'Pass!' if self.CanoeData[1]['Submerge'] else 'Not Pass!'}"

            tk.Label(self.DisplayTable_PageMain_Frame, text=VolumeString, font=(
                "Time", 12, "bold")).grid(column=0, row=1)
            tk.Label(self.DisplayTable_PageMain_Frame, text=WeightSrting, font=(
                "Time", 12, "bold")).grid(column=0, row=2)
            tk.Label(self.DisplayTable_PageMain_Frame, text=BuoyancyString, font=(
                "Time", 12, "bold")).grid(column=0, row=3)
            tk.Label(self.DisplayTable_PageMain_Frame, text=FlowString, font=(
                "Time", 12, "bold")).grid(column=0, row=4)
            tk.Label(self.DisplayTable_PageMain_Frame, text=Submerge, font=(
                "Time", 12, "bold")).grid(column=0, row=5)

            # Model related

            # Generate the canoe
            # consider the example from https://pypi.org/project/numpy-stl/
            window = pyplot.figure()
            canvas = pyplot.subplot(projection="3d")
            # render
            canvas.add_collection3d(mplot3d.art3d.Poly3DCollection(self.canoe_mesh_object.vectors))

            scale = self.canoe_mesh_object.points.flatten()
            canvas.auto_scale_xyz(scale, scale, scale)

            pyplot.show()

        except:
            messagebox.showMessage("Wrong Data Input")
            self.DisplayTable_PageMain_Frame.destroyAllElement()
            self.Save_Button.destroy()
            self.DisplayTable_PageMain()

    def Return(self):
        self.CDD.DeleteData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.DisplayTable_PageMain_Frame.destroy()
        MainGUI_Init(self.master)

    def DeleteLabelatEntry(self, UserLabel, sectionNum, row):
        UserLabel[sectionNum][row].destroy()

    def DireteDeletLabel(self, Labelobj):
        Labelobj.destroy()

    def AssignPreviousInput(self, size, EntryList, UserLabel):
        # Assign the PrePair Table
        # This is really just GUI structure of the page
        # a lot
        # suffer to read
        # can skip

        for createInput in range(size):
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text=f"Section {createInput + 1}",
                     font=("Time", 15, "bold")).grid(column=createInput * 3, row=0)
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text="Canoe Length :", font=(
                    "Time", 12, "")).grid(column=createInput * 3, row=1)
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text="Canoe Width :", font=(
                    "Time", 12, "")).grid(column=createInput * 3, row=2)
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text="Canoe Depth :", font=(
                    "Time", 12, "")).grid(column=createInput * 3, row=3)
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text="Curve Exp:",
                     font=(
                         "Time", 12, "")).grid(column=createInput * 3, row=4)
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text="Width Exp:",
                     font=(
                         "Time", 12, "")).grid(column=createInput * 3, row=5)
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text="Depth Exp:",
                     font=(
                         "Time", 12, "")).grid(column=createInput * 3, row=6)
            tempEntryList = []
            tempEntryList.append(tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                          command=self.buildCommand_Delete(UserLabel, createInput, 0),
                                          deflautReturn=self.InputFile['Length'][createInput]))
            tempEntryList.append(tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                          command=self.buildCommand_Delete(UserLabel, createInput, 1),
                                          deflautReturn=self.InputFile['Width'][createInput]))
            tempEntryList.append(tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                          command=self.buildCommand_Delete(UserLabel, createInput, 2),
                                          deflautReturn=self.InputFile['Depth'][createInput]))
            tempEntryList.append(tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                          command=self.buildCommand_Delete(UserLabel, createInput, 3),
                                          deflautReturn=self.InputFile['ECurveF'][createInput]))
            tempEntryList.append(tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                          command=self.buildCommand_Delete(UserLabel, createInput, 4),
                                          deflautReturn=self.InputFile['EWidthF'][createInput]))
            tempEntryList.append(tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                          command=self.buildCommand_Delete(UserLabel, createInput, 5),
                                          deflautReturn=self.InputFile['EDepthF'][createInput]))
            EntryList.append(tempEntryList)
            tempUserLabel = []
            tempUserLabel.append(tk.Label(self.DisplayTable_PageMain_Frame,
                                          text=f"{self.InputFile['Length'][createInput]}",
                                          font=(
                                              "Time", 10, "")))
            tempUserLabel.append(tk.Label(self.DisplayTable_PageMain_Frame,
                                          text=f"{self.InputFile['Width'][createInput]}",
                                          font=(
                                              "Time", 10, "")))
            tempUserLabel.append(tk.Label(self.DisplayTable_PageMain_Frame,
                                          text=f"{self.InputFile['Depth'][createInput]}",
                                          font=(
                                              "Time", 10, "")))
            tempUserLabel.append(tk.Label(self.DisplayTable_PageMain_Frame,
                                          text=f"{self.InputFile['ECurveF'][createInput]}",
                                          font=(
                                              "Time", 10, "")))
            tempUserLabel.append(tk.Label(self.DisplayTable_PageMain_Frame,
                                          text=f"{self.InputFile['EWidthF'][createInput]}",
                                          font=(
                                              "Time", 10, "")))
            tempUserLabel.append(tk.Label(self.DisplayTable_PageMain_Frame,
                                          text=f"{self.InputFile['EDepthF'][createInput]}",
                                          font=(
                                              "Time", 10, "")))
            UserLabel.append(tempUserLabel)

        # Assign Other Spec's GUI display

        CoverLengthEntry = tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                    command=lambda: [self.DireteDeletLabel(CoverLengthLabel)],
                                    deflautReturn=f"{self.InputFile['CoverLength']}")
        CoverLengthEntry.grid(column=1, row=7)
        DensityEntry = tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                command=lambda: [self.DireteDeletLabel(DensityLabel)],
                                deflautReturn=f"{self.InputFile['Density']}")
        DensityEntry.grid(column=1, row=8)
        ThicknessEntry = tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                  command=lambda: [self.DireteDeletLabel(ThicknessLabel)],
                                  deflautReturn=f"{self.InputFile['Thickness']}")
        ThicknessEntry.grid(column=3, row=7)
        CrewWeightEntry = tk.Entry(self.DisplayTable_PageMain_Frame, width=40, height=15,
                                   command=lambda: [self.DireteDeletLabel(CrewWeightLabel)],
                                   deflautReturn=f"{self.InputFile['CrewWeight']}")
        CrewWeightEntry.grid(column=3, row=8)

        CoverLengthLabel = tk.Label(self.DisplayTable_PageMain_Frame,
                                    text=f"{self.InputFile['CoverLength']}",
                                    font=(
                                        "Time", 10, ""))
        CoverLengthLabel.grid(column=1, row=7)
        tk.Label(self.DisplayTable_PageMain_Frame, text="CoverLength", font=(
            "Time", 10, "")).grid(column=0, row=7)

        DensityLabel = tk.Label(self.DisplayTable_PageMain_Frame,
                                text=f"{self.InputFile['Density']}",
                                font=(
                                    "Time", 10, ""))
        DensityLabel.grid(column=1, row=8)
        tk.Label(self.DisplayTable_PageMain_Frame, text="Density", font=(
            "Time", 10, "")).grid(column=0, row=8)

        ThicknessLabel = tk.Label(self.DisplayTable_PageMain_Frame,
                                  text=f"{self.InputFile['Thickness']}",
                                  font=(
                                      "Time", 10, ""))
        ThicknessLabel.grid(column=3, row=7)
        tk.Label(self.DisplayTable_PageMain_Frame, text="Thickness", font=(
            "Time", 10, "")).grid(column=2, row=7)

        CrewWeightLabel = tk.Label(self.DisplayTable_PageMain_Frame,
                                   text=f"{self.InputFile['CrewWeight']}",
                                   font=(
                                       "Time", 10, ""))
        CrewWeightLabel.grid(column=3, row=8)
        tk.Label(self.DisplayTable_PageMain_Frame, text="CrewWeight", font=(
            "Time", 10, "")).grid(column=2, row=8)

        HallEntryList = [CoverLengthEntry, DensityEntry, ThicknessEntry, CrewWeightEntry]
        return HallEntryList

    def buildCommand_Delete(self, Target, Row, Col):
        return lambda: [self.DeleteLabelatEntry(Target, Row, Col)]


class MainGUI_Optimization():
    def __init__(self, master, InputFilePath):
        self.master = master
        self.InputFile_Path = InputFilePath

        SectionDictObject = {}
        HullListObject = []
        self.CDD = CanoeDataBase(SectionDictObject, HullListObject)
        self.creatWidgets_PageMain()

    def creatWidgets_PageMain(self):
        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue", height=70)
        self.MainGUI_Menu_Button.pack(fill="x")

        self.Return_Button = tk.Button(
            self.MainGUI_Menu_Button, bg="gray", height=70, width=60, image=MainGUI_Init.img_resized_Return,
            command=self.Return)
        self.Return_Button.pack(anchor="w", padx=10, pady=5)

        self.MainGUI_Title = tk.Frame(self.master, height=70)
        self.MainGUI_Title.pack(fill="x", pady=10)
        self.username_label = tk.Label(self.MainGUI_Title, text="", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=30)

        self.DisplayTable_PageMain()

    def DisplayTable_PageMain(self):

        self.MainGUI_Title.configure(bg="green")
        self.username_label.configure(text="Determine Optimize Variable")
        self.DisplayTable_PageMain_Frame = tk.Frame(self.master, height=600, width=self.master.geometry[0])

        self.CDDR = {"Interval": 0.125, "Section": 1,
                     "ECurveF": [], "EDepthF": {0: []}, "EWidthF": {0: []}}

        with open(self.InputFile_Path, "r") as InputFile:
            self.InputFile = eval(InputFile.read())

        # Make sure the size is larger than 0
        size = len(self.InputFile["Length"])

        Section = {}
        Hall = [self.InputFile["CoverLength"],
                self.InputFile["Density"],
                self.InputFile["Thickness"],
                self.InputFile["CrewWeight"]]
        for index in range(size):
            Section[index] = [self.InputFile["Length"][index],
                              self.InputFile["Width"][index],
                              self.InputFile["Depth"][index],
                              self.InputFile["ECurveF"][index],
                              self.InputFile["EWidthF"][index],
                              self.InputFile["EDepthF"][index], ]

        self.CDDR["Section"] = size

        self.DisplayTable_PageMain_Frame.columnconfigure((size * 3) + 1, 5, weight=1)
        self.DisplayTable_PageMain_Frame.pack(pady=50)

        ButtonSectionList = []
        # For Exponent of Curve
        self.ExponentCuvreButton = tk.Button(master=self.DisplayTable_PageMain_Frame, text="Exponent of Curve",
                                             width=100, height=50, command=lambda: [self.CreatRange_Curve()])
        self.ExponentCuvreButton.grid(1, 1)
        for createVariable in range(size):
            self.CDDR["EWidthF"][createVariable] = []
            self.CDDR["EDepthF"][createVariable] = []
            tempButtonList = []
            tempButtonList.append(
                tk.Button(master=self.DisplayTable_PageMain_Frame, text="Exponent of Width", width=100, height=50,
                          command=self.buildCommand_config(createVariable, 0, ButtonSectionList,
                                                           "EWidthF")))
            tempButtonList.append(
                tk.Button(master=self.DisplayTable_PageMain_Frame, text="Exponent of Width", width=100, height=50,
                          command=self.buildCommand_config(createVariable, 1, ButtonSectionList,
                                                           "EDepthF")))
            ButtonSectionList.append(tempButtonList)
        for col, ButtonList in enumerate(ButtonSectionList):
            for row, Button in enumerate(ButtonList):
                Button.grid(col * 3 + 1, row + 2)
        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, bg="gray", image=MainGUI_Init.img_resized_NextPage, width=60,
            height=self.MainGUI_Menu_Button.height - 10,
            command=lambda: [self.FileTransfer(Section, Hall), self.ResultTable_PageMain()])
        self.NextPage_Button.pack(anchor="e", pady=5, padx=10)

    def ResultTable_PageMain(self):
        self.NextPage_Button.destroy()
        self.DisplayTable_PageMain_Frame.destroyAllElement()
        self.MainGUI_Title.configure(bg="red")
        self.username_label.configure(text="Display Optimization report")

        for element in self.CDDR["EWidthF"]:
            if (self.CDDR["EWidthF"][element] == []):
                self.CDDR["EWidthF"][element] = [self.CDD.SDD[element][4],
                                                 self.CDD.SDD[element][4] + self.CDDR["Interval"]]
        for element in self.CDDR["EDepthF"]:
            if (self.CDDR["EDepthF"][element] == []):
                self.CDDR["EDepthF"][element] = [self.CDD.SDD[element][5],
                                                 self.CDD.SDD[element][5] + self.CDDR["Interval"]]
            # Set Default ECurveF
        if (self.CDDR["ECurveF"] == []):
            self.CDDR["ECurveF"] = [self.InputFile["ECurveF"][0],
                                    self.InputFile["ECurveF"][0] + self.CDDR["Interval"]]


        try:
            self.OCCO = OptimizationCalculation(self.CDD, self.CDDR)
            Top3list, ResultLog = self.OCCO.Optimization()
            size = len(self.InputFile["Length"])
            tk.Label(self.DisplayTable_PageMain_Frame,
                     text=f"Top Three Optimize Design from {ResultLog} result",
                     font=(
                         "Time", 15, "")).grid(column=1, row=0)

            tempdict = self.CDD.SDD
            DCCOList = []
            MCCOList = []

            # ready for generate Data Result
            for indexLabel, design in enumerate(Top3list):
                ExpTuple: tuple = ()
                for indexSet, (ECF, ECW, ECD) in enumerate(zip(design[1][0], design[1][1], design[1][2])):
                    tempdict[indexSet][3] = ECF
                    tempdict[indexSet][4] = ECW
                    tempdict[indexSet][5] = ECD
                    ExpTuple = (ECF, ECW, ECD)
                self.CDD.SDD = tempdict
                DCCOList.append(DataCalculation(self.CDD))
                MCCOList.append(ModelCalculation(self.CDD))
                DCCOList[-1].CanoeDataCalculation()
                # Print out Current Data
                logInt, CanoeData, OperationNote = DCCOList[-1].CalDataReturn()

                # Canoe Hall type defined
                tk.Label(self.DisplayTable_PageMain_Frame,
                         text=f"Top {indexLabel + 1} ({ExpTuple})",
                         font=(
                             "Time", 12, "")).grid(column=indexLabel * size + 0.5, row=1)

                # Output display
                VolumeString = f"Volume :{round(CanoeData[1]['Volume'], 2)} cu in"
                WeightSrting = f"Weight :{round(CanoeData[1]['Weight'], 2)} lbs"
                BuoyancyString = f"Buoyancy :{round(CanoeData[1]['Buoyancy'], 2)} N"

                tk.Label(self.DisplayTable_PageMain_Frame, text=VolumeString, font=(
                    "Time", 12, "bold")).grid(column=indexLabel * size + 0.5, row=2)
                tk.Label(self.DisplayTable_PageMain_Frame, text=WeightSrting, font=(
                    "Time", 12, "bold")).grid(column=indexLabel * size + 0.5, row=3)
                tk.Label(self.DisplayTable_PageMain_Frame, text=BuoyancyString, font=(
                    "Time", 12, "bold")).grid(column=indexLabel * size + 0.5, row=4)

                tk.Button(
                    self.DisplayTable_PageMain_Frame, image=MainGUI_Init.img_resized_Save,
                    command=lambda: [self.DisplayAndSave(MCCOList[-1], logInt, CanoeData, OperationNote)],
                    destroySelf=True, height=70, width=60).grid(indexLabel * size + 0.5, row=5)
            





        except:
            messagebox.showMessage("Fail to Optimize")
            self.Return()

    def DisplayAndSave(self, model, logInt, CanoeData, OperationNote):

        # Model related
        canoe_mesh_object = model.Model_Generate()
        # Generate the canoe
        # consider the example from https://pypi.org/project/numpy-stl/
        window = pyplot.figure()
        canvas = pyplot.subplot(projection="3d")
        # render
        canvas.add_collection3d(mplot3d.art3d.Poly3DCollection(canoe_mesh_object.vectors))

        scale = canoe_mesh_object.points.flatten()
        canvas.auto_scale_xyz(scale, scale, scale)

        pyplot.show()

        # Save the Model position by asking
        Folderpath = filedialog.askdirectory(title="Save STL Model")
        if (Folderpath == ""):
            return 0
        # Directly Save Design
        self.CDD.SaveDataIntoFile(OperationNote, CanoeData, logInt)
        filename = OperationNote[-1].split("-> ")[-1] + "_Canoe.stl"
        filePath = f"{Folderpath}/{filename}"
        print(f"Model Save @ {Folderpath}/{filename}")
        self.CDD.SaveStlIntoFile(filePath, canoe_mesh_object)

    def FileTransfer(self, EntryListSection, HallEntryList):

        self.CDD = CanoeDataBase(EntryListSection, HallEntryList)
        self.DCCO = DataCalculation(self.CDD)
        self.MCCO = ModelCalculation(self.CDD)

    def buildCommand_config(self, SectionNum, target, TargetList, Name):
        return lambda: [TargetList[SectionNum][target].configure(bg="yellow"
        if TargetList[SectionNum][target].bg == None else None),
                        self.CreateRange_WidthDepth(SectionNum, Name)]

    def CreateRange_WidthDepth(self, SectionNum, Name):
        mid = self.InputFile[Name][SectionNum]
        if (mid + self.CDDR["Interval"] * 3 < 1):
            if (mid - self.CDDR["Interval"] * 3 >= 0):
                self.CDDR[Name][SectionNum] = [mid - 3 * self.CDDR["Interval"],
                                               mid + 3 * self.CDDR["Interval"]] \
                    if self.CDDR[Name].get(SectionNum, None) == None \
                       or self.CDDR[Name][SectionNum] == [] else []
            else:
                self.CDDR[Name][SectionNum] = [0 + self.CDDR["Interval"],
                                               mid + 3 * self.CDDR["Interval"]] \
                    if self.CDDR[Name].get(SectionNum, None) == None \
                       or self.CDDR[Name][SectionNum] == [] else []
        else:
            self.CDDR[Name][SectionNum] = [0 + self.CDDR["Interval"],
                                           1] \
                if self.CDDR[Name].get(SectionNum, None) == None \
                   or self.CDDR[Name][SectionNum] == [] else []

    def CreatRange_Curve(self):
        mid = self.InputFile["ECurveF"][0]
        if (mid - 3 > 0):
            self.CDDR["ECurveF"] = [mid - 3, mid + 3] if self.CDDR["ECurveF"] == [] else []
        else:
            self.CDDR["ECurveF"] = [mid, mid + 3] if self.CDDR["ECurveF"] == [] else []
        self.ExponentCuvreButton.configure(bg="yellow" if self.ExponentCuvreButton.bg == None else None)

    def Return(self):
        self.CDD.DeleteData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.DisplayTable_PageMain_Frame.destroy()
        MainGUI_Init(self.master)


if __name__ == "__main__":
    root = tk.Tk()

    MainGUI_Base(root)
    root.mainloop()
