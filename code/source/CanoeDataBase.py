import csv
import json
import os
import platform
from datetime import datetime
from pathlib import Path

import matplotlib
import quantities as pq
from pylatex import *
from pylatex.utils import *

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
        CanoeDataDict = saveText[1]
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
        self.ReportGenerate(f"Design_{str(logName)}", UserInput, CanoeDataDict, CanoeDetailDataDict)

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
        self.ReportGenerate(fileName, UserInput, CanoeDataDict, CanoeDetailDataDict)

    def ReportGenerate(self, fileName, UserInput, CanoeDataDict, CanoeDetailDataDict):

        # set up the user Input
        if len(UserInput[0]) == 3:
            semi = UserInput[0][0]
            semi[0] = semi[0]/2
            UserInput[0] = {0.0: semi, 1.0: semi, "Name":UserInput[0]["Name"], "Config_Count": UserInput[0]["Config_Count"]}

            semi_surface = CanoeDetailDataDict["Surface Area by Sections"][0]/2
            CanoeDetailDataDict["Surface Area by Sections"] = [semi_surface,semi_surface,CanoeDetailDataDict["Surface Area by Sections"][1]]

            semi_Outside = CanoeDetailDataDict["Volume_Outside"][0]/2
            CanoeDetailDataDict["Volume_Outside"] = [semi_Outside,semi_Outside,CanoeDetailDataDict["Volume_Outside"][1]]

            semi_Inside = CanoeDetailDataDict["Volume_Inside"][0]/2
            CanoeDetailDataDict["Volume_Inside"] = [semi_Inside,semi_Inside,CanoeDetailDataDict["Volume_Inside"][1]]


        # -------------Main Property----------------
        geometry_options = {"margin": "0.7in"}
        self.doc = Document(geometry_options=geometry_options)

        # Font Style
        self.doc.append(pylatex.Command('selectfont'))
        self.doc.append(pylatex.Command('fontsize', arguments=['12', '15']))

        # self.doc.packages.append(Package('geometry', options=['tmargin=1cm', ]))
        self.doc.packages.append(Package('amsmath'))
        CanoeDataDict = list(CanoeDataDict.values())

        # ---------------Header---------------------
        # Add document header
        header = PageStyle("fancy")
        # Create right header
        with header.create(Head("R")):
            header.append(simple_page_number())
        with header.create(Head("L")):
            header.append(f'Design Serial Number: {UserInput[0]["Name"]}')
        self.doc.preamble.append(header)
        self.doc.change_document_style("fancy")
        # ---------------Header---------------------

        # ---------------Title----------------
        self.doc.preamble.append(Command('title', f'Canoe Design Report'))
        self.doc.preamble.append(Command('author', f'automatically generated by Canoe Design Program'))
        self.doc.preamble.append(Command('date', datetime.now()))
        self.doc.append(NoEscape(r'\maketitle'))
        self.doc.change_page_style("fancy")
        # ---------------Title----------------------

        # ---------------Table----------------------

        formula_list = self.DesignReport(UserInput, CanoeDataDict, CanoeDetailDataDict)
        self.CalculationReprot(UserInput, CanoeDataDict, CanoeDetailDataDict, formula_list)

        # ---------------Table----------------------
        self.doc.generate_pdf(filepath=str(Path(f"../../asset/DesignReport/{fileName}")), compiler="pdflatex",
                              clean_tex=False)
        print(f"Design Report {fileName} Generated")

    def CalculationReprot(self, UserInput, CanoeDataDict, CanoeDetailDataDict, formula_list):
        with self.doc.create(Section("Canoe Calculation Process")):
            self.doc.append("Canoe Design Program automize multiples process of Calculation, including: ")
            with self.doc.create(Itemize()) as itemize:
                itemize.add_item(NoEscape(r"Volume of \textbf{Canoe}, \textbf{Concrete}, \textbf{Styrofoam}"))
                itemize.add_item("Surface Area")
                itemize.add_item("Weight")
                itemize.add_item("Buoyancy")
                itemize.add_item("Capability")
            self.doc.append("Calculation Method, Formula and Process are as follows: ")
            self.calculationMedthodGenerate()
            self.formulalistGenerate(UserInput, CanoeDetailDataDict)
            self.OtherCalculation(UserInput, CanoeDataDict, CanoeDetailDataDict)

    def calculationMedthodGenerate(self):

        with self.doc.create(Subsection("Calculation Method")):
            self.doc.append(
                "The Hull Design Team mainly applied Calculus in the calculation process. Including following concepst:")
            with self.doc.create(Itemize()) as itemize:
                itemize.add_item("Calculus")
                itemize.add_item("Integration")
                itemize.add_item("Differential Equation")

            with self.doc.create(Subsubsection("Explanation")):
                self.doc.append(
                    NoEscape(
                        r"Integration of function is the process of finding the area under the curve of a function, "
                        r"which is donated by \eqref{X}. "))
                self.doc.append(
                    NoEscape(r"And the Area of CrossSection is donated by:"))
                self.doc.append(Command("begin", "align"))
                self.doc.append(NoEscape(r"Define:A &\equiv CrossSection Shape factor\notag\\"))
                self.doc.append(NoEscape(
                    r"Area &=Width\times Depth - \int_0^{Width} (Depth\times(\frac{x}{Width})^{A} \mathrm{d}x\label{A}\\"))
                self.doc.append(NoEscape(r"Area &=Width\times Depth - \frac{Width\times Depth}{A + 1}\notag\\"))
                self.doc.append(NoEscape(r"Area &=\frac{A\times Width\times Depth}{A + 1}\tag{\ref{A}{a}}"))
                self.doc.append(Command("end", "align"))
                self.doc.append(NoEscape(r"Where $a$ is the shape factor of the cross section."))

                self.doc.append(
                    NoEscape(r"We know the Width and Depth is governed by Length as \eqref{Y} and \eqref{Z}."))
                self.doc.append(
                    "Thus, the Length-Aspect Volumn Formula is the Area under the curve of CrossSection Area Function. Donated by: ")
                self.doc.append(Command("begin", "align"))
                self.doc.append(NoEscape(r"Define: B &\equiv Length to Width Shape factor\notag\\"))
                self.doc.append(NoEscape(r"Define: C &\equiv Length to Depth Shape factor\notag\\"))
                self.doc.append(NoEscape(
                    r"Volume &=2\times \displaystyle\sum_{i=0}^{Length} \frac{A\times Width(i) \times Depth(i)}{A+1}\notag\\"))
                self.doc.append(NoEscape(
                    r"Volume &=2\times \frac{A}{A+1} \int_0^{Length} Width\times(\frac{x}{Length})^{B}\times Depth\times(\frac{x}{Length})^{C} \mathrm{d}x\label{B}"))
                self.doc.append(Command("end", "align"))

    def formulalistGenerate(self, UserInput, CanoeDetailDataDict):
        thickness = UserInput[1][2]
        with self.doc.create(Subsection("Formula List")):
            sectionLabelList = ["Front Section Volume Formula", "Middle Section Volume Formula",
                                "Back Section Volume Formula"] \
                if len(UserInput[0]) == 5 else ["Front Section Volume Formula", "Back Section Volume Formula"]
            itemList = ["Length", "Width", "Depth",
                        "A", "B", "C"]
            for sectionIndex, label in enumerate(sectionLabelList):
                formula_specific = r"Volume &=2\times \frac{A}{A+1} \int_0^{Length} Width\times(\frac{x}{Length})^{B}\times Depth\times(\frac{x}{Length})^{C} \mathrm{d}x \notag"
                outside_formula_specific = r"Volume &=2\times \frac{A}{A+1} \int_0^{Length} Width\times(\frac{x}{Length})^{B}\times Depth\times(\frac{x}{Length})^{C} \mathrm{d}x \notag"
                with self.doc.create(Subsubsection(label)):
                    for itemIndex, item in reversed(list(enumerate(itemList))):
                        if item in formula_specific:
                            if item == "Width":
                                formula_specific = formula_specific.replace(item, str(round(
                                    UserInput[0][float(sectionIndex)][itemIndex] / 2, 2)))
                                outside_formula_specific = outside_formula_specific.replace(item, str(round(
                                    UserInput[0][float(sectionIndex)][itemIndex] / 2 + thickness, 2)))
                            else:
                                formula_specific = formula_specific.replace(item, str(round(
                                    UserInput[0][float(sectionIndex)][itemIndex], 2)))

                                if (label != "Middle Section Volume Formula" and itemIndex<=2):
                                    outside_formula_specific = outside_formula_specific.replace(item, str(round(
                                        UserInput[0][float(sectionIndex)][itemIndex] + thickness, 2)))
                                else:
                                    outside_formula_specific = outside_formula_specific.replace(item, str(round(
                                        UserInput[0][float(sectionIndex)][itemIndex], 2)))



                    formula_specific = formula_specific.replace("Volume", "Thickness Exclude: " + str(
                            round(CanoeDetailDataDict["Volume_Inside"][sectionIndex], 2)))
                    outside_formula_specific = outside_formula_specific.replace("Volume",
                                                                                    "Thickness Include: " + str(
                                                                                        round(CanoeDetailDataDict[
                                                                                                  "Volume_Outside"][
                                                                                                  sectionIndex], 2)))

                    self.doc.append(Command("begin", "align"))
                    self.doc.append(NoEscape(formula_specific))
                    self.doc.append(Command("end", "align"))
                    self.doc.append(Command("begin", "align"))
                    self.doc.append(NoEscape(outside_formula_specific))
                    self.doc.append(Command("end", "align"))

    def OtherCalculation(self, UserInput, CanoeDataDict, CanoeDetailDataDict):
        with self.doc.create(Subsection("Other Calculation")):
            self.doc.append(NoEscape(r"\textbf{Buoyancy} is donated by: \textbf{AmiArchimedes' principle}"))
            self.doc.append(Command("begin", "align"))
            self.doc.append(
                NoEscape(r"F_{buoyancy} &=\rho_{liquid}\times Volume\times 0.160111447518 \times g\label{C}"))
            self.doc.append(Command("end", "align"))
            self.doc.append(NoEscape(r"\textbf{Weight} is donated by: "))
            self.doc.append(Command("begin", "align"))
            self.doc.append(
                NoEscape(r"Weight_{lbs} &=(\frac{ConcreteVolume_{inch^2}}{1728})\times Density_{feet^3}\label{D}"))
            self.doc.append(Command("end", "align"))
            self.doc.append(NoEscape(r"\textbf{Weight-bearing (Capability)} is donated by: "))
            self.doc.append(Command("begin", "align"))
            self.doc.append(NoEscape(r"Weight_{lbs} &=(\frac{F_{buoyancy}}{g})\times 2.205 \label{E}"))
            self.doc.append(Command("end", "align"))

            self.doc.append(NoEscape(r"\textbf{Predicate} for Floating Test is donated by: "))
            self.doc.append(Command("begin", "align"))
            self.doc.append(NoEscape(
                r"Result &= \forall x\in Capability_{lbs}, \forall y\in TotalWeight_{lbs} (Pass Floating Test \implies x \geq y) \label{E}"))
            self.doc.append(Command("end", "align"))

            self.doc.append(NoEscape(r"\textbf{Predicate} for Submerging Test is donated by: "))
            self.doc.append(Command("begin", "align"))
            self.doc.append(NoEscape(
                r"Result &= \forall x\in SubmergeCapability_{lbs}, \forall y\in Weight_{lbs} (Pass Submerging Test \implies x \geq y) \label{F}"))
            self.doc.append(Command("end", "align"))

        with self.doc.create(Subsubsection("Calculation Detail")):
            physics_formulaList = [r"F_{buoyancy} &=\rho_{liquid}\times Volume\times 0.160111447518 \times g",
                                   r"Weight_{lbs} &=(\frac{ConcreteVolume_{inch^2}}{1728})\times Density_{feet^3}",
                                   r"Capability_{lbs} &=(\frac{F_{buoyancy}}{g})\times 2.205",
                                   r"Result_{flow} &= \forall x\in Capability_{lbs}, \forall y\in TotalWeight_{lbs} (Pass floating test \implies x \geq y)",
                                   r"Result_{submerge} &= \forall x\in SubmergeCapability_{lbs}, \forall y\in Weight_{lbs} (Pass submerging test \implies x \geq y)"]
            self.doc.append(Command("begin", "align"))
            for index, formula in enumerate(physics_formulaList):
                if ("F" in formula): formula = formula.replace("F", str(round(CanoeDataDict[1], 2)))
                if ("ConcreteVolume" in formula): formula = formula.replace("ConcreteVolume", str(round(
                    CanoeDetailDataDict["Volume_Concrete"][0], 2)))
                if ("Volume" in formula): formula = formula.replace("Volume", str(round(CanoeDataDict[0], 2)))
                if ("TotalWeight" in formula): formula = formula.replace("TotalWeight", str(round(
                    CanoeDetailDataDict["Total Weight"][0], 2)))
                if ("SubmergeCapability" in formula): formula = formula.replace("SubmergeCapability", str(round(
                    CanoeDetailDataDict["Capability_Submerge"][0], 2)))
                if ("Capability" in formula): formula = formula.replace("Capability",
                                                                        str(round(CanoeDetailDataDict["Capability"][0],
                                                                                  2)))
                if ("Weight" in formula): formula = formula.replace("Weight", str(round(CanoeDataDict[2], 2)))

                if ("Density" in formula): formula = formula.replace("Density", str(UserInput[1][1]))
                if ("Result_{flow}" in formula): formula = formula.replace("Result_{flow}",
                                                                           str(CanoeDataDict[3]) + "_{flow}")
                if ("Result_{submerge}" in formula): formula = formula.replace("Result_{submerge}",
                                                                               str(CanoeDataDict[4]) + "_{submerge}")
                if (index == len(physics_formulaList) - 1):
                    self.doc.append(NoEscape(formula + r"\notag"))
                else:
                    self.doc.append(NoEscape(formula + r"\notag" + r"\\"))
            self.doc.append(Command("end", "align"))

    def DesignReport(self, UserInput, CanoeDataDict, CanoeDetailDataDict):
        with self.doc.create(Section('Canoe Design and Specification')):
            self.doc.append("The Canoe Design and Specification Report is as follow: ")
            self.canoeScaleGenerate(UserInput)
            self.canoeDataGenerate(CanoeDataDict)
            self.canoeDetailedDataGenerate(UserInput, CanoeDetailDataDict)
            formula_list = self.canoeFormulaGenerate(UserInput)
        return formula_list

    def canoeScaleGenerate(self, UserInput):
        with self.doc.create(Subsection('Canoe Scale Specification')):
            thickness = UserInput[1][2]
            totalLength = 2 * thickness  # Thickness of the canoe
            for index in range(len(UserInput[0]) - 2):
                totalLength += UserInput[0][float(index)][0]
            self.doc.append(f'Canoe Total Length: {totalLength} Inch')
            sectionLabelList = ["Front Section Scale", "Middle Section Scale", "Back Section Scale", "Other Specs"] \
                if len(UserInput[0]) == 5 else ["Front Section Scale", "Back Section Scale", "Other Specs"]
            labelList = ["Canoe Length", "Canoe Width", "Canoe Depth",
                         "Cross-Section Shape factor", "Length-to-Width Shape factor",
                         "Length-to-Depth Shape factor"]
            for sectionIndex, sectionLabel in enumerate(sectionLabelList):
                with self.doc.create(Subsubsection(sectionLabel)):
                    with self.doc.create(Tabular('|l|l|', row_height=1.5)) as table:
                        if (sectionLabel != "Other Specs"):
                            table.add_hline()
                            for index, label in enumerate(labelList):
                                text = f'{UserInput[0][float(sectionIndex)][index]}'
                                if (index <= 2): text = f'{UserInput[0][float(sectionIndex)][index] + thickness} Inch'
                                if (index == 1): text = f'{UserInput[0][float(sectionIndex)][index] + thickness * 2} Inch'
                                if (index == 0 and sectionLabel == "Middle Section Scale"): text = f'{UserInput[0][float(sectionIndex)][index]} Inch'
                                table.add_row((label, text))
                                table.add_hline()
                        else:
                            specialLabelList = ["Concrete Density", "Concrete Thickness", "Crew Weight"]
                            table.add_hline()
                            for index, label in enumerate(specialLabelList):
                                text = f'{UserInput[1][index + 1]}'
                                if index == 0: text += " Cubic Feet/lb"
                                if index == 1: text += " Inch"
                                if index == 2: text += " lbs"
                                table.add_row((label, text))
                                table.add_hline()

    def canoeDataGenerate(self, CanoeDataDict):
        with self.doc.create(Subsection('Canoe Data Specification')):
            labelList = [["Canoe Volume", "Cubic Inch"], ["Canoe Buoyancy", pq.newton], ["Canoe Weight", pq.pound],
                         ["Canoe Flow Test Boolean", ""], ["Canoe Submerge Test Boolean", ""]]
            with self.doc.create(Tabular('|l|l|')) as table:
                table.add_hline()
                for index, label in enumerate(labelList):
                    value = CanoeDataDict[index]
                    if type(value) in [int, float]: value = round(value, 4)
                    if (type(label[1]) != str):
                        data = value * label[1]

                        table.add_row((label[0], data.rescale(label[1])))
                    else:
                        table.add_row((label[0], f'{value} {label[1]}'))

                    table.add_hline()

    def canoeDetailedDataGenerate(self, UserInput, CanoeDetailDataDict):
        with self.doc.create(Subsection('Canoe Detailed Data')):
            labelList = [["Hull Type", ""], ["Hull Property", ""], ["Hull subProperty", ""],
                         ["Surface Area", "Square Inch"],
                         ["Volume_Styrofoam", "Cubic Inch"], ["Volume_Concrete", "Cubic Inch"],
                         ["Total Weight", pq.pound],
                         ["Buoyancy_Submerge", pq.newton], ["Capability", pq.pound], ["Capability_Submerge", pq.pound]]
            with self.doc.create(Tabular('|l|l|')) as table:
                table.add_hline()
                for index, label in enumerate(labelList):
                    value = CanoeDetailDataDict[label[0]]

                    if (type(value) in [list, tuple]): value = value[0]
                    if type(value) in [int, float]: value = round(value, 4)
                    if (type(label[1]) != str):
                        data = value * label[1]

                        table.add_row(("Canoe " + label[0], data.rescale(label[1])))
                    else:
                        table.add_row(("Canoe " + label[0], f'{value} {label[1]}'))

                    table.add_hline()
            sectionLabelList = ["Front Section Data", "Middle Section Data", "Back Section Data"] \
                if len(UserInput[0]) == 5 else ["Front Section Data", "Back Section Data"]
            sectionValueLabelList = [["Surface Area by Sections", "Square Inch"], ["Volume_Outside", "Cubic Inch"],
                                     ["Volume_Inside", "Cubic Inch"]]
            sectionValueLabelDict = {"Surface Area by Sections": "SurfaceArea",
                                     "Volume_Outside": "Volume (Thickness Included)",
                                     "Volume_Inside": "Volumes (Thickness Excluded)"}
            for sectionIndex, sectionLabel in enumerate(sectionLabelList):
                with self.doc.create(Subsubsection(sectionLabel)):
                    with self.doc.create(Tabular('|l|l|')) as table:
                        table.add_hline()
                        for index, label in enumerate(sectionValueLabelList):
                            value = CanoeDetailDataDict[label[0]][sectionIndex]
                            if type(value) in [int, float]: value = round(value, 4)
                            if (type(label[1]) != str):
                                data = value * label[1]
                                table.add_row(("Canoe " + sectionValueLabelDict[label[0]], data.rescale(label[1])))
                            else:
                                table.add_row(("Canoe " + sectionValueLabelDict[label[0]], f'{value} {label[1]}'))
                            table.add_hline()

    def canoeFormulaGenerate(self, UserInput):
        formula_list = []
        with self.doc.create(Subsection('Canoe Detailed Data')):
            self.doc.append("The Mathematical representation of the Canoe is as follows: ")
            self.doc.append("\n")

            formulaList = [
                r"CrossSection(x) = Depth\times(\frac{x}{Width})^{CrossSection Shape factor} \label{X}",
                r"width(x) = Width\times(\frac{x}{Length})^{Length to Width Shape factor} \label{Y}",
                r"depth(x) = Depth\times(\frac{x}{Length})^{Length to Depth Shape factor} \label{Z}"]
            for formula in formulaList:
                self.doc.append(Command("begin", "equation"))
                self.doc.append(NoEscape(formula))
                self.doc.append(Command("end", "equation"))

            self.doc.append("\n")
            self.doc.append(NoEscape(r"The General Formula for Cross-Section is donated by \eqref{X}"))
            self.doc.append("\n")
            self.doc.append(
                NoEscape(r"The General Formula for Cross-Section's Width at Length x is donated by \eqref{Y}"))
            self.doc.append("\n")
            self.doc.append(
                NoEscape(r"The General Formula for Cross-Section's Depth at Length x is donated by \eqref{Z}"))
            self.doc.append("\n")

            sectionLabelList = ["Front", "Middle", "Back"] \
                if len(UserInput[0]) == 5 else ["Front", "Back"]
            itemList = ["Length", "Width", "Depth",
                        "CrossSection Shape factor", "Length to Width Shape factor", "Length to Depth Shape factor"]
            for index, label in enumerate(sectionLabelList):
                with self.doc.create(Subsubsection(label + "Section Mathematical Representation")):
                    for formula in formulaList:
                        formula_notation = []
                        for itemIndex, item in reversed(list(enumerate(itemList))):
                            if item in formula:
                                if item == "Width":
                                    formula = formula.replace(item,
                                                              str(round(UserInput[0][float(index)][itemIndex] / 2, 2)))
                                else:
                                    formula = formula.replace(item,
                                                              str(round(UserInput[0][float(index)][itemIndex], 2)))

                        if "\label{X}" in formula:
                            formula = formula.replace("\label{X}",
                                                      r"\tag{\ref{X}{" + chr(index + 97) + "}}")  # chr(97) = a
                            formula_notation.append(r"\tag{\ref{X}{" + chr(index + 97) + "}}")
                        if "\label{Y}" in formula:
                            formula = formula.replace("\label{Y}",
                                                      r"\tag{\ref{Y}{" + chr(index + 97) + "}}")  # chr(97) = a
                            formula_notation.append(r"\tag{\ref{Y}{" + chr(index + 97) + "}}")
                        if "\label{Z}" in formula:
                            formula = formula.replace("\label{Z}",
                                                      r"\tag{\ref{Z}{" + chr(index + 97) + "}}")  # chr(97) = a
                            formula_notation.append(r"\tag{\ref{Z}{" + chr(index + 97) + "}}")
                        formula_list.append(formula_notation)

                        self.doc.append(Command("begin", "equation"))
                        self.doc.append(NoEscape(formula))
                        self.doc.append(Command("end", "equation"))
        return formula_list

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
