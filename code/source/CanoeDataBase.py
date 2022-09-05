import csv
import json
import os
import platform
from pathlib import Path


class CanoeDataBase:
    # Designed to connect to STL database

    def __init__(self, SectionDataDict, HullDataList):
        self.SDD = SectionDataDict
        self.HDL = HullDataList
        self.SymmetryBoolean = False
        self.FSDMode = False

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

    def GetSYM(self):
        return (self.SymmetryBoolean)

    def GetFSD(self):
        return (self.FSDMode)

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
        del self.SDD
        del self.HDL

    def SaveDataToSQL(self):
        # Save Data To SQL
        print('work')

    def WriteDataIntoFile(self, CSVAddress, LogAddress, saveText, logName, GraphSet):
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

        # Generate file name
        fileName = f"{DesignNumber}"
        for l in logInt:
            fileName += str(l)

        # Save Model
        Stlfilename = OperationNote[-1].split("-> ")[-1] + f"_{fileName}" + "_Canoe.stl"
        StlfilePath = f"{STLfilePath}/{Stlfilename}"
        print(f"Model Save @ {STLfilePath}/{Stlfilename}")
        self.SaveStlIntoFile(StlfilePath, STLobj)

        # Save User Input for Open
        UserInput = [CanoeData[0].SDD, CanoeData[0].HDL]
        UserInput[0]["Name"] = fileName
        self.DesignHistoryLog = Path(f'..//..//asset//__designHistory//__log{fileName}.txt')

        with open(self.DesignHistoryLog, "w") as Userlog:
            Userlog.write(json.dumps(UserInput))

        # OutPutCSVFile
        fileName = "Design_" + fileName
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

    def SaveGraphIntoFile(self, fileName, GraphSet):
        FolderPath = Path(f"..//..//asset//ModelGraph//{fileName}_ConstructionGraph_Canoe")
        # Make the HullFolder
        os.makedirs(FolderPath)
        for index, section_graph in enumerate(GraphSet):
            section_path = Path(f"..//..//asset//ModelGraph//{fileName}_ConstructionGraph_Canoe//section_{index}")
            os.makedirs(section_path)
            for crossSection in section_graph:
                graph_path = Path(
                    f"..//..//asset//ModelGraph//{fileName}_ConstructionGraph_Canoe//section_{index}//inch_{crossSection[1]}.png")
                crossSection[0].savefig(graph_path, dpi='figure', format="png", pad_inches=0)

    def SaveStlIntoFile(self, filePath, stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)

    @staticmethod
    def SaveStlIntoFile_static(filePath, stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)
