import json
import os
import csv

import Messagebox112


class CanoeDataBase:
    # Design to be the bridge between MainGUI and Calculation
    def __init__(self, SectionDataDict, HullDataList):
        self.SDD = SectionDataDict
        self.HDL = HullDataList
        self.SymmetryBoolean = False

    def ConstructDict_SDD(self, SectionNum, DataList):
        self.SDD[SectionNum] = DataList

    def ConstructDict_HDL(self, DataList):
        self.HDL = DataList

    def GetData_SDD(self):
        return (self.SDD)

    def GetData_CDD(self):
        return (self.SDD, self.HDL)

    def GetExponent(self,num):
        return (self.SDD[num][3],self.SDD[num][4],self.SDD[num][5])

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

    def WriteDataIntoFile(self,CSVAddress,LogAddress,saveText, logName):
        CanoeDetailDataDict = saveText[2]
        try:
            with open(CSVAddress + '.csv', "w") as CSV:
                writer = csv.writer(CSV)
                for key, value in CanoeDetailDataDict.items():
                    if (type(value) in [tuple, list, set]):
                        writeIn = [key] + value
                        writer.writerow(writeIn)
                    else:
                        writer.writerow([key, value])
            UserInput = saveText[0]
            UserInput['Name'] = "__log" + str(logName)
            with open(LogAddress, "w") as Userlog:
                Userlog.write(json.dumps(UserInput))
            Messagebox112.showMessage("File Config Complete")
        except:
            Messagebox112.showMessage("Permission Denied B/C the file is opened")





    def SaveDataIntoFile(self, DesignLog, saveText, logInt):

        # re-load the software Log
        with open("..\\..\\asset\\progressSave\\__log.txt", "r") as log:
            logString = eval(log.read())
            DesignNumber = logString["Canoe Design"] + 1
            onebodyCount = logString["One Body Design"]
            twobodyCount = logString["Two Body Design"]
            threebodyCount = logString["Three Body Design"]
            if ("One Body" in DesignLog[0]):
                onebodyCount += 1
            elif ("Two Body" in DesignLog[0]):
                twobodyCount += 1
            elif ("Three Body" in DesignLog[0]):
                threebodyCount += 1

        logString = {"Canoe Design": DesignNumber, "One Body Design": onebodyCount, "Two Body Design": twobodyCount,
                     "Three Body Design": threebodyCount}

        with open("..\\..\\asset\\progressSave\\__log.txt", "w") as log:
            log.write(json.dumps(logString))

        # Covert saveText (dict) to csv file


        # Generate file name
        fileName = f"{DesignNumber}"
        for l in logInt:
            fileName += str(l)




        # Save User Input for Open
        UserInput = saveText[0]
        UserInput["Name"] = fileName

        with open(f'..\\..\\asset\\__designHistory\\__log{fileName}.txt', "w") as Userlog:
            Userlog.write(json.dumps(UserInput))

        # OutPutCSVFile
        fileName = "Design_" + fileName
        CanoeDetailDataDict = saveText[2]
        fileAddress = f"..\\..\\asset\\progressSave\\{fileName}"
        with open(f'{fileAddress}.csv', 'w') as CSV:

            writer = csv.writer(CSV)
            for key, value in CanoeDetailDataDict.items():
                if (type(value) in [tuple, list, set]):
                    writeIn = [key] + value
                    writer.writerow(writeIn)
                else:
                    writer.writerow([key, value])
        AbsFilePath = __file__
        AbsFilePath = AbsFilePath[0:AbsFilePath.index("Code")]
        AbsFilePath += f"asset\\progressSave\\{fileName}"

        print(f"Save Design File At {AbsFilePath}")

    def SaveStlIntoFile(self, filePath, stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)

    @staticmethod
    def SaveStlIntoFile_static(filePath, stlObject):

        print(f"File Save @ {filePath}")
        stlObject.save(filePath)
