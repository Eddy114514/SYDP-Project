import csv
import json
import platform
from pathlib import Path
import os
from datetime import datetime
from pylatex import *
from pylatex.utils import italic


import matplotlib
# Remove the following line if you want to use the default matplotlib backend (line 9)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.axis('off')
from PIL import Image, ImageOps
import numpy as np



# This part is to get the DPI of the device that excutes the code.
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
screen = app.screens()[0]
DPI_OF_DEVICE = screen.physicalDotsPerInch()
app.quit()

# This class will be used to store the data of the canoe and manipulate the output of the program.
# The CanoeDataBase Object will be used to connect MainGUI.py and Calculate.py.
class CanoeDataBase:
    # Designed to connect to STL database

    def __init__(self, SectionDataDict, HullDataList, B1=False, B2=False, B3=False):
        self.SDD = SectionDataDict
        self.HDL = HullDataList
        self.SymmetryBoolean = B1
        self.FSDMode = B2
        self.Construction = B3

    def ConfigSYM(self):
        print("Change from ", self.SymmetryBoolean)
        # flap the Boolean
        self.SymmetryBoolean = not self.SymmetryBoolean
        print("to", self.SymmetryBoolean)

    def ConfigFSD(self):
        print("Change from ", self.FSDMode)
        # flap the Boolean
        self.FSDMode = not self.FSDMode
        print("to", self.FSDMode)

    def ConfigConstruction(self):
        print("Change from ", self.Construction)
        # flap the Boolean
        self.Construction = not self.Construction
        print("to", self.Construction)

    def GetSYM(self):
        return (self.SymmetryBoolean)

    def GetFSD(self):
        return (self.FSDMode)

    def GetConstruction(self):
        return self.Construction

    def ConstructDict_SDD(self, SectionNum, DataList):
        self.SDD[SectionNum] = DataList

    def ConstructDict_HDL(self, DataList):
        self.HDL = DataList

    def GetData_SDD(self):
        return (self.SDD)

    def GetData_CDD(self):
        return (self.SDD, self.HDL)

    def DeleteData_SDD(self):
        del self.SDD

    def DeleteData_HDL(self):
        del self.HDL

    def DeleteData_CDD(self):
        # delete all data and reset all setting
        del self.SDD
        del self.HDL
        self.SymmetryBoolean = False
        self.FSDMode = False
        self.Construction = False

    def SaveDataToSQL(self):
        # Save Data To SQL
        print('work')

    def WriteDataIntoFile(self, CSVAddress, LogAddress, saveText, logName, Config_Count, GraphSet):
        CanoeDetailDataDict = saveText[2]
        with open(CSVAddress, "w") as CSV:
            writer = csv.writer(CSV)
            for key, value in CanoeDetailDataDict.items():
                if (type(value) in [tuple, list, set]):
                    writeIn = [key] + value
                    writer.writerow(writeIn)
                else:
                    writer.writerow([key, value])
        UserInput = [saveText[0].SDD, saveText[0].HDL]
        UserInput[0]['Name'] = str(logName)
        UserInput[0]["Config_Count"] = Config_Count
        with open(LogAddress, "w") as Userlog:
            Userlog.write(json.dumps(UserInput))
        # TODO Give the log a count function that save the time of configuration on it, default is zero

        self.SaveGraphIntoFile(f"Design_{str(logName)}", GraphSet)
    def SaveDataIntoFile(self, OperationNote, CanoeData, logInt, STLfilePath, STLobj, GraphSet):

        # re-load the software Log
        self.FilePathlog = Path("..//..//asset//progressSave//__log.txt")

        with open(self.FilePathlog, "r") as log:
            logString = eval(log.read())
            DesignNumber = logString["Canoe Design"] + 1
            onebodyCount = logString["One Body Design"]
            twobodyCount = logString["Two Body Design"]
            threebodyCount = logString["Three Body Design"]
            if ("One Body" in OperationNote[0]):
                onebodyCount += 1
            elif ("Two Body" in OperationNote[0]):
                twobodyCount += 1
            elif ("Three Body" in OperationNote[0]):
                threebodyCount += 1

        logString = {"Canoe Design": DesignNumber, "One Body Design": onebodyCount, "Two Body Design": twobodyCount,
                     "Three Body Design": threebodyCount}

        with open(self.FilePathlog, "w") as log:
            log.write(json.dumps(logString))

        # Covert saveText (dict) to csv file

        # Generate the file name
        fileName = f"{DesignNumber}"
        for l in logInt[0:3]:
            fileName += str(l)

        # Save Model
        Stlfilename = OperationNote[-1].split("-> ")[-1] + f"_{fileName}" + "_Canoe.stl"
        StlfilePath = f"{STLfilePath}/{Stlfilename}"
        print(f"Model Save @ {STLfilePath}/{Stlfilename}")
        self.SaveStlIntoFile(StlfilePath, STLobj)

        # Save User Input for Open
        UserInput = [CanoeData[0].SDD, CanoeData[0].HDL]
        UserInput[0]["Name"] = fileName
        UserInput[0]["Config_Count"] = 0
        self.DesignHistoryLog = Path(f'..//..//asset//__designHistory//__log{fileName}.txt')

        with open(self.DesignHistoryLog, "w") as Userlog:
            Userlog.write(json.dumps(UserInput))

        # OutPutCSVFile
        fileName = "Design_" + fileName
        CanoeDataDict = CanoeData[1]
        CanoeDetailDataDict = CanoeData[2]
        self.fileAddress = Path(f"..//..//asset//progressSave//{fileName}")

        with open(f'{self.fileAddress}.csv', 'w') as CSV:

            writer = csv.writer(CSV)
            for key, value in CanoeDetailDataDict.items():
                if (type(value) in [tuple, list, set]):
                    writeIn = [key] + value
                    writer.writerow(writeIn)
                else:
                    writer.writerow([key, value])
        AbsFilePath = __file__
        AbsFilePath = AbsFilePath[0:AbsFilePath.index("code")]
        AbsFilePath = AbsFilePath[:-1] + f"/asset/progressSave/{fileName}" \
            if platform.system().lower() == 'windows' \
            else AbsFilePath + f"\\asset\\progressSave\\{fileName}"

        print(f"Save Design File At {AbsFilePath}")

        # SaveGraph
        self.SaveGraphIntoFile(fileName, GraphSet)

        # Save PDF


    def SaveGraphIntoFile(self, fileName, GraphSet):
        if (GraphSet == 42):
            return 42

        FolderPath = Path(f"..//..//asset//ModelGraph//{fileName}_ConstructionGraph_Canoe")
        # Make the HullFolder
        os.makedirs(FolderPath)
        for index, section_graph in enumerate(GraphSet):
            section_path = Path(f"..//..//asset//ModelGraph//{fileName}_ConstructionGraph_Canoe//section_{index}")
            os.makedirs(section_path)
            for crossSection in section_graph:
                graph_path = Path(
                    f"..//..//asset//ModelGraph//{fileName}_ConstructionGraph_Canoe//section_{index}//inch_{crossSection[-1][1]}.png")
                self.Graph_Generate_Save(crossSection[-1], crossSection[0], crossSection[1], graph_path)

    def Graph_Generate_Save(self, title, X, Y, path):
        # 1.Change the graph generate mode to semi
        # 2.When the semi-graph size is larger than some size, automatically cut it in to two graph

        # PrintOut Data
        # print out the coordinate through terminal
        print(f"Cross-Section at {title[1]}, formula = {title[0]}")

        Positive_X = []
        Positive_Y = []
        for index, (x, y) in enumerate(zip(X, Y)):
            # print the coordinate through terminal of each point of cross-section.
            print(f"X: {round(x, 8)} || Y: {round(y, 8)}")
            if (x >= 0):
                Positive_X.append(x)
                Positive_Y.append(y)
        print("\n")
        index = path.__str__().index(".png")  # replace the png
        splitPathStr = path.__str__()[0: index]  # + f"_{count_index}" + ".png"
        curve_formula = lambda x: title[2][0] * (x ** title[2][1])

        scale_factor = 7.25
        scale_x = [0, 7.25]
        scale_y = [0, 7.25]

        x_value = np.linspace(0, Positive_X[-1], 100)
        y_value = title[-1][0] * (x_value ** title[-1][1])

        # 1.1 Generate the graph
        if (Positive_X[-1] > scale_factor or Positive_Y[-1] > scale_factor):
            # 1.2 Cut the graph if the Y is larger than 7.25 inch or X is larger than 7.25 inch.
            # Because the graph is too large to be printed out in a A4 paper.
            # This algorithm will cut the graph into two graph and print them out in two A4 paper.
            if (Positive_X[-1] > scale_factor):
                for x_index, x_factor in enumerate(range(int(Positive_X[-1] / scale_factor) + 1)):
                    x_range_low = x_factor * scale_factor
                    x_range_high = x_range_low + scale_factor

                    scale_x = [x_range_low, x_range_high]
                    y_low = curve_formula(x_range_low)
                    y_high = curve_formula(x_range_high) if Positive_X[-1] > x_range_high else curve_formula(
                        Positive_X[-1])

                    for y_index, y_factor in enumerate(range(int(y_high / scale_factor) + 1)):
                        y_range_low = y_factor * scale_factor
                        y_range_high = y_range_low + scale_factor
                        if (y_low <= y_range_high):
                            scale_y = [y_range_low, y_range_high]
                            splitPath = Path(splitPathStr + f"_Part[{x_index}x{y_index}]" + ".png")
                            self.DrawGraph(x_value, y_value, splitPath, scale_x, scale_y, title)
            # 1.2 Generate the graph when the Y is within the scale factor
            else:
                y_point = curve_formula(Positive_X[-1])
                for y_index, y_factor in enumerate(range(int(y_point / scale_factor) + 1)):
                    y_range_low = y_factor * scale_factor
                    y_range_high = y_range_low + scale_factor
                    scale_y = [y_range_low, y_range_high]
                    splitPath = Path(splitPathStr + f"_Part[{0}x{y_index}]" + ".png")
                    self.DrawGraph(x_value, y_value, splitPath, scale_x, scale_y, title)


        else:

            self.DrawGraph(x_value, y_value, path, scale_x, scale_y, title)

    def DrawGraph(self, x_value, y_value, path, scale_x, scale_y, title):
        # Draw Graph
        left_margin = 0.25  # inch
        right_margin = 0.25  # inch
        figure_width = 7.5  # inch
        figure_height = 7.5  # inch
        top_margin = 1.75  # inch
        bottom_margin = 1.75  # inch

        box_width = left_margin + figure_width + right_margin
        box_height = top_margin + figure_height + bottom_margin

        # specifying the width and the height of the box in inches
        fig = plt.figure(figsize=(box_width, box_height))
        ax = fig.add_subplot(111)
        ax.plot(x_value, y_value)
        plt.title(f"Cross-Section at {title[1]}, formula = {title[2][0]}x^{title[2][1]}")

        fig.subplots_adjust(left=left_margin / box_width,
                            bottom=bottom_margin / box_height,
                            right=1. - right_margin / box_width,
                            top=1. - top_margin / box_height,
                            )

        plt.xlim(scale_x[0], scale_x[1])
        plt.ylim(scale_y[0], scale_y[1])
        plt.savefig(path, format="png", dpi=DPI_OF_DEVICE)
        plt.close()

        im = Image.open(rf"{path}")
        flip = ImageOps.mirror(im)
        index = path.__str__().index(".png")  # replace the png
        splitPathStr = path.__str__()[0: index]
        left_save = Path(splitPathStr + "_left" + ".png")
        right_save = Path(splitPathStr + "_right" + ".png")

        im.save(right_save)
        flip.save(left_save)
        os.remove(path)










    def SaveStlIntoFile(self, filePath, stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)

    @staticmethod
    def SaveStlIntoFile_static(filePath, stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)
