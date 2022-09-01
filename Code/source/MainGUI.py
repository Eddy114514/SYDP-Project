import tkinter as tk
from pathlib import Path
from tkinter import simpledialog
from tkinter import StringVar
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d

# Import other files
from HealthCheck import *


class MainGUI_Base():
    # read startUp file
    address = '..\\..\\asset\\startSetup\\setUpinformation.txt' \
        if platform.system().lower() == "windows" \
        else '..//..//asset//startSetup//setUpinformation.txt'

    with open(address) as dict:
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
            self.root.geometry("1400x800")
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
        with Image.open('../../asset/Picture/CreatNew_Icon.png') as CreatNew:
            img_CreatNew = CreatNew.resize((80, 100), Image.ANTIALIAS)
            self.img_resized_CreatNew = ImageTk.PhotoImage(img_CreatNew)

        with Image.open('../../asset/Picture/Cut_Icon.png') as Cut:
            img_Cut = Cut.resize((80, 100), Image.ANTIALIAS)
            self.img_resized_Cut = ImageTk.PhotoImage(img_Cut)

        with Image.open('../../asset/Picture/Open_Icon.png') as Open:
            img_Open = Open.resize((80, 100), Image.ANTIALIAS)
            self.img_resized_Open = ImageTk.PhotoImage(img_Open)

        with Image.open('../../asset/Picture/FindBest_Icon.png') as Findbest:
            img_Findbest = Findbest.resize((80, 100), Image.ANTIALIAS)
            self.img_resized_Findbest = ImageTk.PhotoImage(img_Findbest)

        with Image.open('../../asset/Picture/Menu_Icon.png') as Return:
            img_Return = Return.resize((50, 50), Image.ANTIALIAS)
            MainGUI_Init.img_resized_Return = ImageTk.PhotoImage(img_Return)

        with Image.open('../../asset/Picture/Add_Icon.png') as Add:
            img_Add = Add.resize((50, 50), Image.ANTIALIAS)
            MainGUI_Init.img_resized_Add = ImageTk.PhotoImage(img_Add)

        with Image.open('../../asset/Picture/NextPage_Icon.png') as NextPage:
            img_NextPage = NextPage.resize((50, 50), Image.ANTIALIAS)
            MainGUI_Init.img_resized_NextPage = ImageTk.PhotoImage(img_NextPage)

        with Image.open('../../asset/Picture/BackPage_Icon.png') as BackPage:
            img_BackPage = BackPage.resize((50, 50), Image.ANTIALIAS)
            MainGUI_Init.img_resized_BackPage = ImageTk.PhotoImage(img_BackPage)

        with Image.open('../../asset/Picture/Save_Icon.png') as Save:
            img_Save = Save.resize((50, 50), Image.ANTIALIAS)
            MainGUI_Init.img_resized_Save = ImageTk.PhotoImage(img_Save)

    def CreateWidgets(self):
        # username_label
        tk.Label(self.MainGUI_Init_MainFrame, text="Canoe Design Program", font=(
            "Time", 15, "bold")).pack(pady=10)

        # CreatNew_Button
        tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_CreatNew, text="New Project", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwitch_CreatNew).pack(pady=40)

        # Open_Button
        tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_Open, text="Open Project", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwitch_Open).pack(pady=40)

        # CreatNew_Button
        tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_Findbest, text="Design Optimization", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwitch_FindBest).pack(pady=40)

        # Cut_Button
        tk.Button(self.MainGUI_Init_MainFrame, image=self.img_resized_Cut, text="Canoe Cut", font=(
            "Time", 15, "bold"), compound=tk.LEFT, command=self.PgSwitch_Cut).pack(pady=0)

        # Debug Button
        self.Debug_Button = tk.Button(
            self.MainGUI_Init_MainFrame, text="Debug",
            command=lambda: [MainGUI_Base.dB.ChangDebug(True), sys.exit()])
        self.Debug_Button.pack(side="bottom", padx=10, pady=self.master.winfo_height() * (3 / 4))

    def PgSwitch_CreatNew(self):
        self.MainGUI_Init_MainFrame.destroy()
        MainGUI_Init.CreatNewWindow = MainGUI_CreatNEW(self.master)

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

    def PgSwitch_Cut(self):
        InputFile_Path = self.GetFilePath()
        Cut_Inch = simpledialog.askfloat('CutInchInput',"How much do you want to cut (inch)")

        if (InputFile_Path != ""):
            self.MainGUI_Init_MainFrame.destroy()
            MainGUI_Cut(self.master, InputFile_Path,Cut_Inch)

    def GetFilePath(self):
        AbsFilePath = __file__
        AbsFilePath = AbsFilePath[0:AbsFilePath.index("code")]
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
            messagebox.showwarning("Wrong Folder Choice")
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

        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue")
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master)
        self.MainGUI_Title.pack(fill="x", pady=50)
        self.username_label = tk.Label(self.MainGUI_Title, text="", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=10)

        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage,
            command=lambda: [self.SaveData(MainGUI_CreatNEW.Num_Counter, MainGUI_CreatNEW.Page_Counter),
                             self.NextPage()])
        self.NextPage_Button.pack(side="right", padx=10, pady=10)

    # SON is PageConditionBoolean
    # STR is PageConditionKeyword
    def creatWidgets_PageOne(self, SON, STR="Null"):

        if (SON == False):
            self.MainGUI_InputTable = None
            self.Return_Button = 0

        if (SON == True):

            SectionDictObject = {}
            HullDictObject = []
            self.CDD = CanoeDataBase(SectionDictObject, HullDictObject)
            self.MainGUI_Title.configure(bg="green")
            self.username_label.configure(text="Data Input Table (1)")

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
            self.MainGUI_InputTable_Two = tk.Frame(self.master)
            self.MainGUI_InputTable_Two.columnconfigure(0, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(1, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(2, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(4, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(5, weight=3)
            self.MainGUI_InputTable_Two.columnconfigure(6, weight=3)
            self.MainGUI_InputTable_Two.pack(fill="x", pady=150)
            self.DataInputTable_PageTWO()
            self.BackPage_Button = tk.Button(self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_BackPage,
                                             command=lambda: [
                                                 self.PreviousPage_One()])
            self.BackPage_Button.pack(side="left", padx=10, pady=10)
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

            self.MainGUI_DisplayTable_Three = tk.Frame(self.master)
            self.MainGUI_DisplayTable_Three.columnconfigure(0, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(1, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(2, weight=3)
            self.MainGUI_DisplayTable_Three.columnconfigure(3, weight=3)
            self.MainGUI_DisplayTable_Three.pack(fill="both", expand=True)

            self.NextPage_Button.destroy()

            self.BackPage_Button = tk.Button(self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_BackPage,
                                             command=lambda: [
                                                 self.PreviousPage_Two()])
            self.BackPage_Button.pack(side="left", padx=10, pady=10)

            self.Save_Button = tk.Button(
                self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Save,
                command=lambda: [self.FileAcquire(),
                                 self.returnToMainPageAcquire()])  # Acquire File and call CanoeDateBase
            self.Save_Button.pack(side="right", padx=10, pady=10)

            self.DisplayTable_PageThree()

            if (STR == "Update"):
                self.FrameStoreList[2][0] = self.MainGUI_DisplayTable_Three
                self.FrameStoreList[2][1] = self.BackPage_Button
                self.FrameStoreList[2][2] = self.Save_Button

    def DataInputTable(self, NumCount):
        # Defind Input table

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
                                          NumCount / 2) + 1),
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
                       / 2][0].grid(column=NumCount + 1, row=2, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][1].grid(column=NumCount + 1, row=3, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][2].grid(column=NumCount + 1, row=4, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][3].grid(column=NumCount + 1, row=5, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][4].grid(column=NumCount + 1, row=6, sticky=tk.W)
        self.EntryDict[NumCount
                       / 2][5].grid(column=NumCount + 1, row=7, sticky=tk.W)

        self.AddNewTable_Button = tk.Button(
            self.MainGUI_InputTable, image=MainGUI_Init.img_resized_Add,
            command=lambda: [self.Addtable(True, NumCount)])
        self.AddNewTable_Button.grid(
            column=NumCount + 2, row=2, sticky=tk.W, padx=10)

        if (NumCount == 4):
            print("work5")
            self.Symmetry_CheckButton = tk.Checkbutton(
                self.MainGUI_InputTable, command=lambda: [self.CDD.ConfigSYM()], text="Symmetricity: ", font=(
                    "Time", 12))
            self.Symmetry_CheckButton.grid(
                column=NumCount + 2, row=1, sticky=tk.W, padx=10)

    def DataInputTable_PageTWO(self):
        self.CoverLength_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.Density_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.Thickness_entry = tk.Entry(self.MainGUI_InputTable_Two)
        self.CrewWeight_entry = tk.Entry(self.MainGUI_InputTable_Two)

        # CoverLenth_Label
        tk.Label(self.MainGUI_InputTable_Two, text="Cover Length :", font=(
            "Time", 12)).grid(column=0, row=1, sticky=tk.E, ipady=5, ipadx=5)
        # Density_Label
        tk.Label(self.MainGUI_InputTable_Two, text="Concrete Density :", font=(
            "Time", 12)).grid(column=0, row=2, sticky=tk.E, ipady=5, ipadx=5)
        # Thickness_Label
        tk.Label(self.MainGUI_InputTable_Two, text="Concrete Thickness :", font=(
            "Time", 12)).grid(column=0, row=3, sticky=tk.E, ipady=5, ipadx=5)
        # CrewWeight_Label
        tk.Label(self.MainGUI_InputTable_Two, text="CrewWeight :", font=(
            "Time", 12)).grid(column=0, row=4, sticky=tk.E, ipadx=5, ipady=5)
        tk.Checkbutton(self.MainGUI_InputTable_Two, text="FSD Mode",
                       command=lambda: [self.CDD.ConfigFSD()]).grid(column=0, row=5, sticky=tk.E, ipadx=5, ipady=5)

        self.CoverLength_entry.grid(column=1, row=1, sticky=tk.W)
        self.Density_entry.grid(column=1, row=2, sticky=tk.W)
        self.Thickness_entry.grid(column=1, row=3, sticky=tk.W)
        self.CrewWeight_entry.grid(column=1, row=4, sticky=tk.W)

    def DisplayTable_PageThree(self):
        try:
            self.DCCO = DataCalculation(self.CDD)  # DataCalculationCanoeObject
            self.MCCO = ModelCalculation(self.CDD)  # ModelCalculationCanoeObject
            # Action
            self.DCCO.CanoeDataCalculation()
            # Print out Current Data
            self.logInt, self.CanoeData, self.OperationNote = self.DCCO.CalDataReturn()

            # Output display
            VolumeString = f"Canoe Volume :{round(self.CanoeData[1]['Volume'], 2)} cubic inch"
            WeightSrting = f"Canoe Weight :{round(self.CanoeData[1]['Weight'], 2)} lbs"
            BuoyancyString = f"Canoe Buoyancy :{round(self.CanoeData[1]['Buoyancy'], 2)} N"
            FlowString = f"Flow Test :{'Pass!' if self.CanoeData[1]['Flow'] else 'Not Pass!'}"
            Submerge = f"Submerge Test: {'Pass!' if self.CanoeData[1]['Submerge'] else 'Not Pass!'}"

            tk.Label(self.MainGUI_DisplayTable_Three, text="Result", font=(
                "Time", 12, "bold")).grid(column=0, row=0, sticky=tk.SW, ipadx=5, ipady=5)

            tk.Label(self.MainGUI_DisplayTable_Three, text=VolumeString, font=(
                "Time", 12, "bold")).grid(column=0, row=1, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.MainGUI_DisplayTable_Three, text=WeightSrting, font=(
                "Time", 12, "bold")).grid(column=0, row=2, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.MainGUI_DisplayTable_Three, text=BuoyancyString, font=(
                "Time", 12, "bold")).grid(column=0, row=3, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.MainGUI_DisplayTable_Three, text=FlowString, font=(
                "Time", 12, "bold")).grid(column=0, row=4, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.MainGUI_DisplayTable_Three, text=Submerge, font=(
                "Time", 12, "bold")).grid(column=0, row=5, sticky=tk.W, ipadx=5, ipady=5)

            self.canoe_mesh_object = self.MCCO.Model_Generate()
            # Create a new plot

            fig = Figure(figsize=(3, 3),
                         dpi=100)
            axes = fig.add_subplot(111, projection="3d")
            # Render the canoe
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.canoe_mesh_object.vectors))

            scale = self.canoe_mesh_object.points.flatten()
            print(scale)
            axes.auto_scale_xyz(scale, scale, scale)
            axes.set_xlabel("X axis")
            axes.set_ylabel("Y axis")
            axes.set_zlabel("Z axis")

            canvas = FigureCanvasTkAgg(fig, self.MainGUI_DisplayTable_Three)
            canvas.draw()
            canvas.get_tk_widget().grid(column=3, row=0)
        except:
            messagebox.showwarning(message="Invalid Input")
            self.MainGUI_DisplayTable_Three.destroy()
            self.MainGUI_InputTable_Two.destroy()

            self.Return()

    def Addtable(self, booleanTable=0, NumCount=0):
        if (booleanTable and NumCount < 4):

            self.SaveData(NumCount / 2, MainGUI_CreatNEW.Page_Counter)
            NumCount += 2
            self.AddNewTable_Button.destroy()
            self.DataInputTable(NumCount)
            MainGUI_CreatNEW.Num_Counter = NumCount / 2
            print(MainGUI_CreatNEW.Num_Counter)

        elif (booleanTable and NumCount == 4):
            self.SaveData(NumCount / 2, MainGUI_CreatNEW.Page_Counter)
            self.AddNewTable_Button.destroy()
            print(MainGUI_CreatNEW.Num_Counter)
            messagebox.showinfo("information", "Reach The MAX Section Number")

    def FileAcquire(self):
        # Save the Model position by asking
        Folderpath = filedialog.askdirectory()
        if (Folderpath == ""):
            return 0
            # No save

        # Directly Save Design

        self.CDD.SaveDataIntoFile(self.OperationNote, self.CanoeData, self.logInt, Folderpath, self.canoe_mesh_object)

    def returnToMainPageAcquire(self):
        answer: bool = messagebox.askyesno(title="Back to the Menu?", message="Want To Return To MainPage?")
        if (answer):
            # delete the data
            self.MainGUI_InputTable_Two.destroy()
            self.MainGUI_DisplayTable_Three.destroy()
            self.Return()

    def SaveData(self, Numcount, PageNum):

        print(Numcount, "Num is ")
        print(PageNum)

        if (Numcount <= 2 and PageNum == 0):
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
        MainGUI_CreatNEW.Page_Counter = 0
        MainGUI_CreatNEW.Num_Counter = 0
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
        self.CDD.DeleteData_HDL()
        MainGUI_CreatNEW.Num_Counter -= 1
        for FrameObject in self.FrameStoreList[MainGUI_CreatNEW.Page_Counter]:
            FrameObject.destroy()
        MainGUI_CreatNEW.Page_Counter = MainGUI_CreatNEW.Page_Counter - 1
        self.PageStoreList[MainGUI_CreatNEW.Page_Counter](True, "Update")
        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage,
            command=lambda: [self.SaveData(MainGUI_CreatNEW.Num_Counter, MainGUI_CreatNEW.Page_Counter),
                             self.NextPage()])
        self.NextPage_Button.pack(side="right", padx=10, pady=10)


class MainGUI_Open():
    def __init__(self, master, InputFilePath):
        self.master = master
        self.InputFile_Path = InputFilePath
        SectionDictObject = {}
        HullListObject = []
        self.CDD = CanoeDataBase(SectionDictObject, HullListObject)
        self.creatWidgets_PageMain()

    def creatWidgets_PageMain(self):
        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue")
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master)
        self.MainGUI_Title.pack(fill="x", pady=50)
        self.username_label = tk.Label(self.MainGUI_Title, text="", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=10)

        self.Return_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Return, command=self.Return)
        self.Return_Button.pack(side="left", padx=10, pady=10)

        self.DisplayTable_PageMain()

    def DisplayTable_PageMain(self):
        self.MainGUI_Title.configure(bg="green")
        self.username_label.configure(text="Past Input")
        self.DisplayTable_PageMain_Frame = tk.Frame(self.master)

        with open(self.InputFile_Path, "r") as InputFile:
            self.InputFile = eval(InputFile.read())

        self.size = len(self.InputFile[0]) - 1
        for add in range((3 * self.size) + 1):
            self.DisplayTable_PageMain_Frame.columnconfigure(add, weight=3)

        self.DisplayTable_PageMain_Frame.pack(fill="both", expand=True)

        # Store the Entry
        entry_section_list = []
        # Store the UserLabel

        hall_entry_list = self.AssignPreviousInput(self.size, entry_section_list)
        # CreateOtherPart

        self.Next_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage,
            command=lambda: [
                self.FileTransfer(entry_section_list, hall_entry_list)])  # Acquire File and call CanoeDateBase
        self.Next_Button.pack(side="right", padx=10, pady=10)

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
            messagebox.showwarning("Wrong Config")
            self.DisplayTable_PageMain_Frame.destroy()
            self.Next_Button.destroy()
            self.DisplayTable_PageMain()

    def FileConfig(self):
        # Save the model at first
        Folderpath = filedialog.askdirectory(title="Save STL Model")
        filename = self.OperationNote[-1].split("-> ")[-1] + f"_{self.InputFile[0]['Name']}-config" + "_Canoe.stl"
        if (Folderpath != ""):
            filePath = f"{Folderpath}/{filename}"
            print(f"Model Save @ {Folderpath}/{filename}")
            self.CDD.SaveStlIntoFile(filePath, self.canoe_mesh_object)

        FileName = self.InputFile[0]["Name"]
        FileAddress = Path(f"..//..//asset//progressSave//{'Design_' + FileName}.csv")

        self.CDD.WriteDataIntoFile(FileAddress, self.InputFile_Path, self.CanoeData, self.InputFile[0]['Name'])

    def ResultTableDisplay(self):
        self.DisplayTable_PageMain_Frame.destroy()
        self.Next_Button.destroy()

        # GUI construct

        self.Save_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Save,
            command=lambda: [self.FileConfig(), self.Return()])  # Acquire File and call CanoeDateBase
        self.Save_Button.pack(side="right", padx=10, pady=10)

        self.MainGUI_Title.configure(bg="red")
        self.username_label.configure(text="Result Display")

        # Reset The Page
        self.DisplayTable_PageMain_Frame = tk.Frame(self.master)
        self.DisplayTable_PageMain_Frame.columnconfigure(0, weight=3)
        self.DisplayTable_PageMain_Frame.columnconfigure(1, weight=3)
        self.DisplayTable_PageMain_Frame.columnconfigure(2, weight=3)
        self.DisplayTable_PageMain_Frame.columnconfigure(3, weight=3)
        self.DisplayTable_PageMain_Frame.pack(fill="both", expand=True)

        try:
            self.DCCO.CanoeDataCalculation()
            # Print out Current Data
            self.logInt, self.CanoeData, self.OperationNote = self.DCCO.CalDataReturn()

            # Output display
            VolumeString = f"Canoe Volume :{round(self.CanoeData[1]['Volume'], 2)} cubic inch"
            WeightSrting = f"Canoe Weight :{round(self.CanoeData[1]['Weight'], 2)} lbs"
            BuoyancyString = f"Canoe Buoyancy :{round(self.CanoeData[1]['Buoyancy'], 2)} N"
            FlowString = f"Flow Test :{'Pass!' if self.CanoeData[1]['Flow'] else 'Not Pass!'}"
            Submerge = f"Submerge Test: {'Pass!' if self.CanoeData[1]['Submerge'] else 'Not Pass!'}"

            tk.Label(self.DisplayTable_PageMain_Frame, text="Result", font=(
                "Time", 12, "bold")).grid(column=0, row=0, sticky=tk.SW, ipadx=5, ipady=5)

            tk.Label(self.DisplayTable_PageMain_Frame, text=VolumeString, font=(
                "Time", 12, "bold")).grid(column=0, row=1, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.DisplayTable_PageMain_Frame, text=WeightSrting, font=(
                "Time", 12, "bold")).grid(column=0, row=2, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.DisplayTable_PageMain_Frame, text=BuoyancyString, font=(
                "Time", 12, "bold")).grid(column=0, row=3, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.DisplayTable_PageMain_Frame, text=FlowString, font=(
                "Time", 12, "bold")).grid(column=0, row=4, sticky=tk.W, ipadx=5, ipady=5)
            tk.Label(self.DisplayTable_PageMain_Frame, text=Submerge, font=(
                "Time", 12, "bold")).grid(column=0, row=5, sticky=tk.W, ipadx=5, ipady=5)

            self.canoe_mesh_object = self.MCCO.Model_Generate()
            # Create a new plot

            fig = Figure(figsize=(3, 3),
                         dpi=100)
            axes = fig.add_subplot(111, projection="3d")
            # Render the canoe
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.canoe_mesh_object.vectors))

            scale = self.canoe_mesh_object.points.flatten()
            axes.auto_scale_xyz(scale, scale, scale)
            axes.set_xlabel("X axis")
            axes.set_ylabel("Y axis")
            axes.set_zlabel("Z axis")

            canvas = FigureCanvasTkAgg(fig, self.DisplayTable_PageMain_Frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=3, row=0)

        except:
            messagebox.showwarning("Wrong Data Input")
            self.DisplayTable_PageMain_Frame.destroy()
            self.Save_Button.destroy()
            self.DisplayTable_PageMain()

    def Return(self):
        self.CDD.DeleteData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.DisplayTable_PageMain_Frame.destroy()
        MainGUI_Init(self.master)

    def DireteDeletLabel(self, Labelobj):
        Labelobj.destroy()

    def AssignPreviousInput(self, size, EntryList):
        # Assign the PrePair Table
        # This is really just GUI structure of the page
        # a lot
        # suffer to read
        # can skip
        label_list = ["Canoe Length :", "Canoe Width :", "Canoe Depth :",
                      "Exponent of Curve function :",
                      "Exponent of Width function :",
                      "Exponent of Depth function :"]

        StrVarList = []
        for assign in self.InputFile[0]:
            temp = []
            if (assign != "Name"):
                for section in self.InputFile[0][assign]:
                    str = StringVar()
                    str.set(section)
                    temp.append(str)
                StrVarList.append(temp)

        for ColIndex, createInput in enumerate(range(size)):
            tempEntry = []
            # Assign Section Title
            tk.Label(self.DisplayTable_PageMain_Frame, text=f"Section {ColIndex}", font=("Time", 12)).grid(
                column=ColIndex * 3,
                row=0)
            for Rowindex, Labeltext in enumerate(label_list):
                # Assign Label

                tk.Label(self.DisplayTable_PageMain_Frame, text=Labeltext, font=("Time", 12)).grid(column=ColIndex * 3,
                                                                                                   row=Rowindex + 1,
                                                                                                   sticky=tk.E,
                                                                                                   ipady=5, ipadx=5)
                tempEntry.append(
                    tk.Entry(self.DisplayTable_PageMain_Frame, textvariable=StrVarList[ColIndex][Rowindex]))
                tempEntry[-1].grid(column=(ColIndex * 3) + 1, row=Rowindex + 1, sticky=tk.W,
                                   ipady=5, ipadx=5)
            EntryList.append(tempEntry)

        tk.Label(self.DisplayTable_PageMain_Frame, text="Canoe Specs", font=("Time", 12, "bold")).grid(column=0, row=8,
                                                                                                       ipady=20)

        tk.Label(self.DisplayTable_PageMain_Frame, text="Cover Length :", font=("Time", 12)).grid(column=0, row=9,
                                                                                                  sticky=tk.E,
                                                                                                  ipady=5, ipadx=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text="Density :", font=("Time", 12)).grid(column=0, row=10,
                                                                                             sticky=tk.E,
                                                                                             ipady=5, ipadx=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text="Thickness :", font=("Time", 12)).grid(column=2, row=9,
                                                                                               sticky=tk.E,
                                                                                               ipady=5, ipadx=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text="CrewWeight :", font=("Time", 12)).grid(column=2, row=10,
                                                                                                sticky=tk.E,
                                                                                                ipady=5, ipadx=5)

        CovLen = StringVar()
        Density = StringVar()
        Thickness = StringVar()
        CrewWeight = StringVar()

        CovLen.set(self.InputFile[1][0])
        Density.set(self.InputFile[1][1])
        Thickness.set(self.InputFile[1][2])
        CrewWeight.set(self.InputFile[1][3])

        CoverLengthEntry = tk.Entry(self.DisplayTable_PageMain_Frame, textvariable=CovLen)
        DensityEntry = tk.Entry(self.DisplayTable_PageMain_Frame, textvariable=Density)
        ThicknessEntry = tk.Entry(self.DisplayTable_PageMain_Frame, textvariable=Thickness)
        CrewWeightEntry = tk.Entry(self.DisplayTable_PageMain_Frame, textvariable=CrewWeight)
        CoverLengthEntry.grid(row=9, column=1, sticky=tk.W,
                              ipady=5, ipadx=5)
        DensityEntry.grid(row=10, column=1, sticky=tk.W,
                          ipady=5, ipadx=5)
        ThicknessEntry.grid(row=9, column=3, sticky=tk.W,
                            ipady=5, ipadx=5)
        CrewWeightEntry.grid(row=10, column=3, sticky=tk.W,
                             ipady=5, ipadx=5)

        HallEntryList = [CoverLengthEntry, DensityEntry, ThicknessEntry, CrewWeightEntry]

        return HallEntryList


class MainGUI_Optimization():
    def __init__(self, master, InputFilePath):
        self.master = master
        self.InputFile_Path = InputFilePath
        self.creatWidgets_PageMain()

    def creatWidgets_PageMain(self):
        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="blue")
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master)
        self.MainGUI_Title.pack(fill="x", pady=50)
        self.username_label = tk.Label(self.MainGUI_Title, text="", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=10)

        self.Return_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Return, command=self.Return)
        self.Return_Button.pack(side="left", padx=10, pady=10)

        self.DisplayTable_PageMain()

    def DisplayTable_PageMain(self):
        self.MainGUI_Title.configure(bg="green")
        self.username_label.configure(text="Determine Optimize Variable")
        self.DisplayTable_PageMain_Frame = tk.Frame(self.master)

        self.CDDR = {"Interval": 0.125, "Section": 1,
                     "ECurveF": [], "Exponent of Depth": {}, "Exponent of Width": {}}

        with open(self.InputFile_Path, "r") as InputFile:
            self.InputFile = eval(InputFile.read())

        section = self.InputFile[0]
        hall = self.InputFile[1]

        index = 0
        # ensure key is Int
        temp = {}
        for var in section:
            if (var != "Name"):
                temp[index] = section[var]
                index += 1
        section = temp

        self.CDD = CanoeDataBase(section, hall)
        self.CDDR["Section"] = len(section)

        for add in range(len(section)):
            self.DisplayTable_PageMain_Frame.columnconfigure(add, weight=3)
        self.DisplayTable_PageMain_Frame.pack()
        self.DisplayTable_PageMain_Frame.pack(fill="both", expand=True)

        ButtonList = []
        for createVariable in range(len(section)):
            temp = []

            self.CDDR["Exponent of Width"][createVariable] = []
            self.CDDR["Exponent of Depth"][createVariable] = []
            temp.append(tk.Button(self.DisplayTable_PageMain_Frame, text="Exponent of Width",
                                  command=lambda: [], height=3))
            temp.append(tk.Button(self.DisplayTable_PageMain_Frame, text="Exponent of Depth",
                                  command=lambda: [], height=3))
            ButtonList.append(temp)

        self.ExponentCuvreButton = tk.Button(master=self.DisplayTable_PageMain_Frame, text="Exponent of Curve",
                                             command=lambda: [self.CreatRange_Curve()], height=3)
        self.ExponentCuvreButton.grid(column=0, row=1, ipady=15, ipadx=15)
        for colIndex, Blist in enumerate(ButtonList):
            for rowIndex, B in enumerate(Blist):
                B.configure(command=self.buildCommand(B, B.cget("text"), colIndex))
                tk.Label(self.DisplayTable_PageMain_Frame, text=f"Section {colIndex}").grid(row=0, column=colIndex,
                                                                                            ipady=15, ipadx=15)
                B.grid(row=rowIndex + 2, column=colIndex, ipady=15, ipadx=15)

        self.NextPage_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_NextPage,
            command=lambda: [self.ResultTable_PageMain()])
        self.NextPage_Button.pack(side="right", padx=10, pady=10)

    def buildCommand(self, target, name, row):
        return lambda: [target.configure(bg="yellow" if target.cget("bg") != "yellow" else "SystemButtonFace"),
                        self.creatRange(name, row)]

    def ResultTable_PageMain(self):
        self.NextPage_Button.destroy()
        self.DisplayTable_PageMain_Frame.destroy()
        self.MainGUI_Title.configure(bg="red")
        self.username_label.configure(text="Display Optimization report")

        for element in self.CDDR["Exponent of Width"]:
            if (self.CDDR["Exponent of Width"][element] == []):
                self.CDDR["Exponent of Width"][element] = [self.CDD.SDD[element][4],
                                                           self.CDD.SDD[element][4] + self.CDDR["Interval"]]
        for element in self.CDDR["Exponent of Depth"]:
            if (self.CDDR["Exponent of Depth"][element] == []):
                self.CDDR["Exponent of Depth"][element] = [self.CDD.SDD[element][5],
                                                           self.CDD.SDD[element][5] + self.CDDR["Interval"]]
            # Set Default ECurveF
        if (self.CDDR["ECurveF"] == []):
            self.CDDR["ECurveF"] = [self.InputFile["ECurveF"][0],
                                    self.InputFile["ECurveF"][0] + self.CDDR["Interval"]]

        self.DisplayTable_PageMain_Frame = tk.Frame(self.master)
        for add in range(len(self.CDDR["Exponent of Depth"])):
            self.DisplayTable_PageMain_Frame.columnconfigure(add, weight=3)
        self.DisplayTable_PageMain_Frame.pack()
        self.DisplayTable_PageMain_Frame.pack(fill="both", expand=True)

        self.OptResultDisplay()
        """try:
            self.OptResultDisplay()
            
        except:
            messagebox.showwarning(message="Fail to Optimize")
            self.Return()"""

    def OptResultDisplay(self):
        self.OCCO = OptimizationCalculation(self.CDD, self.CDDR)
        Top3list, ResultLog = self.OCCO.Optimization()
        tk.Label(self.DisplayTable_PageMain_Frame,
                 text=f"Top Three Optimize Design from {ResultLog} result",
                 font=(
                     "Time", 15)).grid(column=1, row=0)

        tempdict = self.CDD.SDD
        DCCOList = []
        MCCOList = []
        ButtonList = []
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
                         "Time", 12)).grid(column=indexLabel, row=1)

            # Output display
            VolumeString = f"Volume :{round(CanoeData[1]['Volume'], 2)} cu in"
            WeightSrting = f"Weight :{round(CanoeData[1]['Weight'], 2)} lbs"
            BuoyancyString = f"Buoyancy :{round(CanoeData[1]['Buoyancy'], 2)} N"

            tk.Label(self.DisplayTable_PageMain_Frame, text=VolumeString, font=(
                "Time", 12, "bold")).grid(column=indexLabel, row=2)
            tk.Label(self.DisplayTable_PageMain_Frame, text=WeightSrting, font=(
                "Time", 12, "bold")).grid(column=indexLabel, row=3)
            tk.Label(self.DisplayTable_PageMain_Frame, text=BuoyancyString, font=(
                "Time", 12, "bold")).grid(column=indexLabel, row=4)

            canoe_mesh_object = MCCOList[-1].Model_Generate()
            # Create a new plot

            fig = Figure(figsize=(3, 3),
                         dpi=100)
            axes = fig.add_subplot(111, projection="3d")
            # Render the canoe
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(canoe_mesh_object.vectors))

            scale = canoe_mesh_object.points.flatten()
            axes.auto_scale_xyz(scale, scale, scale)
            axes.set_xlabel("X axis")
            axes.set_ylabel("Y axis")
            axes.set_zlabel("Z axis")

            canvas = FigureCanvasTkAgg(fig, self.DisplayTable_PageMain_Frame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=indexLabel, row=5)

            ButtonList.append(tk.Button(
                self.DisplayTable_PageMain_Frame, image=MainGUI_Init.img_resized_Save,
                command=self.buildCommandSave(OperationNote, CanoeData, logInt, canoe_mesh_object, ButtonList, indexLabel),
                height=70, width=60))
            ButtonList[-1].grid(column=indexLabel, row=6)

    def buildCommandSave(self, OperationNote, CanoeData, logInt, canoe_mesh_object, ButtonList, indexLabel):
        return lambda: [self.FileAcquire(OperationNote, CanoeData, logInt, canoe_mesh_object),
                        ButtonList[indexLabel].destroy()]

    def FileAcquire(self, OperationNote, CanoeData, logInt, canoe_mesh_object):
        # Save the Model position by asking
        Folderpath = filedialog.askdirectory()
        if (Folderpath == ""):
            return 0
            # No save

        # Directly Save Design

        self.CDD.SaveDataIntoFile(OperationNote, CanoeData, logInt, Folderpath, canoe_mesh_object)

    def creatRange(self, Name, SectionNum):

        index = 4 if Name == "Exponent of Width" else 5
        mid = self.CDD.SDD[SectionNum][index]
        if (mid + self.CDDR["Interval"] * 3 < 1):
            if (mid - self.CDDR["Interval"] * 3 > 0):
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
        mid = self.CDD.SDD[0][3]
        if (mid - 3 > 0):
            self.CDDR["ECurveF"] = [mid - 3, mid + 3] if self.CDDR["ECurveF"] == [] else []
        else:
            self.CDDR["ECurveF"] = [mid, mid + 3] if self.CDDR["ECurveF"] == [] else []
        self.ExponentCuvreButton.configure(
            bg="yellow" if self.ExponentCuvreButton.cget("bg") != "yellow" else "SystemButtonFace")

    def Return(self):
        self.CDD.DeleteData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.DisplayTable_PageMain_Frame.destroy()
        MainGUI_Init(self.master)

class MainGUI_Cut():
    def __init__(self, master, InputFilePath, CutInch):
        self.master = master
        self.InputFile_Path = InputFilePath
        self.CutInch = CutInch
        self.creatWidgets_PageMain()

    def creatWidgets_PageMain(self):
        self.MainGUI_Menu_Button = tk.Frame(self.master, bg="red")
        self.MainGUI_Menu_Button.pack(fill="x")

        self.MainGUI_Title = tk.Frame(self.master)
        self.MainGUI_Title.pack(fill="x", pady=50)
        self.username_label = tk.Label(self.MainGUI_Title, text="Cut Result Table", font=(
            "Time", 15, "bold"))
        self.username_label.pack(pady=10)

        self.DisplayTable_PageMain()

    def DisplayTable_PageMain(self):
        with open(self.InputFile_Path, "r") as InputFile:
            self.InputFile = eval(InputFile.read())

        section = self.InputFile[0].copy()
        section.pop("Name")
        print(self.InputFile)

        hall = self.InputFile[1]

        # ensure key is Int
        for var in section:
            newDepth = section[var][2] - self.CutInch
            newWidth = ((newDepth/section[var][2])**(1/section[var][3]))*section[var][1]
            # depth config
            section[var][2] = round(section[var][2] - self.CutInch,2)
            # width config
            section[var][1] = round(newWidth,2)

        self.CDD = CanoeDataBase(section, hall)



        self.DisplayTable_PageMain_Frame = tk.Frame(self.master)
        self.DisplayTable_PageMain_Frame.columnconfigure(0, weight=3)
        self.DisplayTable_PageMain_Frame.columnconfigure(1, weight=3)
        self.DisplayTable_PageMain_Frame.columnconfigure(2, weight=3)
        self.DisplayTable_PageMain_Frame.columnconfigure(3, weight=3)
        self.DisplayTable_PageMain_Frame.pack(fill="both", expand=True)

        self.DCCO = DataCalculation(self.CDD)  # DataCalculation# CanoeObject
        self.MCCO = ModelCalculation(self.CDD)  # ModelCalculationCanoeObject
        # Action
        self.DCCO.CanoeDataCalculation()
        # Print out Current Data
        self.logInt, self.CanoeData, self.OperationNote = self.DCCO.CalDataReturn()

        # Output display
        VolumeString = f"Canoe Volume :{round(self.CanoeData[1]['Volume'], 2)} cubic inch"
        WeightSrting = f"Canoe Weight :{round(self.CanoeData[1]['Weight'], 2)} lbs"
        BuoyancyString = f"Canoe Buoyancy :{round(self.CanoeData[1]['Buoyancy'], 2)} N"
        FlowString = f"Flow Test :{'Pass!' if self.CanoeData[1]['Flow'] else 'Not Pass!'}"
        Submerge = f"Submerge Test: {'Pass!' if self.CanoeData[1]['Submerge'] else 'Not Pass!'}"

        tk.Label(self.DisplayTable_PageMain_Frame, text="Result", font=(
            "Time", 12, "bold")).grid(column=0, row=0, sticky=tk.SW, ipadx=5, ipady=5)

        tk.Label(self.DisplayTable_PageMain_Frame, text=VolumeString, font=(
            "Time", 12, "bold")).grid(column=0, row=1, sticky=tk.W, ipadx=5, ipady=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text=WeightSrting, font=(
            "Time", 12, "bold")).grid(column=0, row=2, sticky=tk.W, ipadx=5, ipady=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text=BuoyancyString, font=(
            "Time", 12, "bold")).grid(column=0, row=3, sticky=tk.W, ipadx=5, ipady=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text=FlowString, font=(
            "Time", 12, "bold")).grid(column=0, row=4, sticky=tk.W, ipadx=5, ipady=5)
        tk.Label(self.DisplayTable_PageMain_Frame, text=Submerge, font=(
            "Time", 12, "bold")).grid(column=0, row=5, sticky=tk.W, ipadx=5, ipady=5)

        self.canoe_mesh_object = self.MCCO.Model_Generate()
        # Create a new plot

        fig = Figure(figsize=(3, 3),
                     dpi=100)
        axes = fig.add_subplot(111, projection="3d")
        # Render the canoe
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.canoe_mesh_object.vectors))

        scale = self.canoe_mesh_object.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)
        axes.set_xlabel("X axis")
        axes.set_ylabel("Y axis")
        axes.set_zlabel("Z axis")

        canvas = FigureCanvasTkAgg(fig, self.DisplayTable_PageMain_Frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=3, row=0)

        self.Save_Button = tk.Button(
            self.MainGUI_Menu_Button, image=MainGUI_Init.img_resized_Save,
            command=lambda: [self.FileConfig(), self.Return()])  # Acquire File and call CanoeDateBase
        self.Save_Button.pack(side="right", padx=10, pady=10)
        """try:
            

        except:
            messagebox.showwarning(message="Invalid Input")
            self.Return()"""

    def Return(self):
        self.CDD.DeleteData_CDD()
        self.MainGUI_Menu_Button.destroy()
        self.MainGUI_Title.destroy()
        self.DisplayTable_PageMain_Frame.destroy()
        MainGUI_Init(self.master)

    def FileConfig(self):
        # Save the model at first
        Folderpath = filedialog.askdirectory(title="Save STL Model")
        filename = self.OperationNote[-1].split("-> ")[-1] + f"_{self.InputFile[0]['Name']}-Cut" + "_Canoe.stl"
        if (Folderpath != ""):
            filePath = f"{Folderpath}/{filename}"
            print(f"Model Save @ {Folderpath}/{filename}")
            self.CDD.SaveStlIntoFile(filePath, self.canoe_mesh_object)

        FileName = self.InputFile[0]["Name"]
        FileAddress = Path(f"..//..//asset//progressSave//{'Design_' + FileName}.csv")

        self.CDD.WriteDataIntoFile(FileAddress, self.InputFile_Path, self.CanoeData, self.InputFile[0]['Name'])




if __name__ == "__main__":
    root = tk.Tk()

    MainGUI_Base(root)
    root.mainloop()
