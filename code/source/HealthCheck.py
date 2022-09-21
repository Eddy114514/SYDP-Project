import json
import os
import platform
import sys
from multiprocessing import Process

from CanoeDataBase import CanoeDataBase
from DataCalculation import DataCalculation
from ModelCalculation import ModelCalculation
from OptimizationCalculation import OptimizationCalculation


class DebugBase:
    address = '..\\..\\asset\\startSetup\\setUpinformation.txt'
    if (platform.system().lower() != 'windows'):
        address = '..//..//asset//startSetup//setUpinformation.txt'

    def __init__(self, debugBoolean):
        self.isDebug = debugBoolean

    def DebugMode(self, Profile):
        self.command_Read(Profile)
        End_Parameter = input("""End the debug mode? Enter: [y/n]""")

        if (End_Parameter == 'n'):
            print("Program End")
            sys.exit()
        elif (End_Parameter == 'y'):  # exit the debug mode and restart
            print("Program End \n Debug Mode Off")
            self.ChangDebug(False)
            self.restartProgram()
        else:
            self.command_Read(Profile)

    def command_Read(self, Profile):
        ProfileList = ['sym', 'lsh', 'sch', 'ach', 'ath']
        print("Press 'help' for debug Instruction")
        while (Profile != " "):
            if (Profile == 'help'):
                print("""
                Press 's' to enter setting mode
                Press 'space' to end the program
                Press 'reset' to reset all saveFile
                        """)
            elif (Profile == 's'):
                print("enter Setting")
                self.configureSetting()
            elif (Profile == "reset"):
                self.ResetAll()

            elif (Profile not in ProfileList):
                Err = 'TestProfile not in the list'
                HealthCheckBase.ErrorReturn(Err)
            else:
                self.DebugTest(Profile)

            # End the Program
            print("Enter 'space' to end the program")
            Profile = input("Enter the TestProfile or 'space':")

    def ResetAll(self):
        # Make sure right fillpath index

        if (platform.system().lower() == 'windows'):
            FilePathlog = '..\\..\\asset\\progressSave\\__log.txt'
            FilePathModel = "..\\..\\asset\\ModelFile"
            FilePathModel1 = "..\\..\\asset\\ModelFile\\"
            DesignHistory = "..\\..\\asset\\__designHistory"
            DesignHistory1 = "..\\..\\asset\\__designHistory\\"
            ProgressSave = "..\\..\\asset\\progressSave"
            ProgressSave1 = "..\\..\\asset\\progressSave\\"
            FilePathGraph = "..\\..\\asset\\ModelGraph"
        else:
            FilePathlog = '././asset/progressSave/__log.txt'
            FilePathModel = "././asset/ModelFile"
            FilePathModel1 = "././asset/ModelFile/"
            DesignHistory = "././asset/__designHistory"
            DesignHistory1 = "././asset/__designHistory/"
            ProgressSave = "././asset/progressSave"
            ProgressSave1 = "././asset/progressSave/"
            FilePathGraph = "././asset/ModelGraph"

        # reset Software Log
        if (input("Reset Software Log? [y/n]") in ["y", "Y"]):
            with open(FilePathlog, "w") as f:
                resetFormat = {"Canoe Design": 0, "One Body Design": 0, "Two Body Design": 0,
                               "Three Body Design": 0}
                f.write(json.dumps(resetFormat))

            # delet all savefiles
        if (input("Delete All Model ? [y/n]") in ["y", "Y"]):
            for file in os.listdir(FilePathModel):
                os.remove(FilePathModel1 + file)
            for file in os.listdir(FilePathGraph):
                try:
                    os.removedirs(FilePathGraph + file)
                except OSError:
                    for file in os.listdir(FilePathGraph):
                        new_path = os.path.join(FilePathGraph, file)
                        if (os.path.isdir(new_path)):
                            self.RecursiveRemoveFolder(new_path)

        if (input("Delete AllHistory ? [y/n]") in ["y", "Y"]):
            for file in os.listdir(DesignHistory):
                os.remove(DesignHistory1 + file)

        if (input("Delete All ProgressSave ? [y/n]") in ["y", "Y"]):
            for file in os.listdir(ProgressSave):
                if ("csv" in file):
                    os.remove(ProgressSave1 + file)

        print("Reset Done")

    def RecursiveRemoveFolder(self, Path):
        try:
            os.removedirs(Path)
        except OSError:
            if (os.path.isdir(Path)):
                for file in os.listdir(Path):
                    newPath = os.path.join(Path, file)
                    if (os.path.isdir(newPath)):
                        self.RecursiveRemoveFolder(newPath)
                    else:
                        # remove all files
                        for file in os.listdir(Path):
                            file_path = os.path.join(Path, file)
                            os.remove(file_path)
                        break

    def configureSetting(self):
        with open(DebugBase.address, 'r') as f:
            startSetUp = eval(f.read())
        for mode, value in startSetUp.items():
            print(f"{mode} = {bool(value)}")
        infor = input("Do You Want Config The Mode? [y/n]")

        changeFlag = False

        while (infor != 'end'):
            if (infor == 'y'):
                changeFlag = self.config(input("Which Mode? (enter the mode string)"), startSetUp)
                print("Enter y to continue Config the setting")
            elif (infor == 'n'):
                break
            print("Enter 'end' to end the Program")
            infor = input()
        # end text
        if (changeFlag):
            if (input("You Made Change, Do You Want To Restart To Apply Configuration? [y/n]") == 'y'):
                sys.exit()
            else:
                print("Return To The DeBug Mode")
        else:
            if (input("You Did Not Made Change, Do You Want To Exit The Debug Mode? [y/n]") == 'y'):
                sys.exit()
            else:
                print("Return To The DeBug Mode")

    @staticmethod
    def config(modeString, startSetUp):
        for operate in modeString.split(' '):
            if (operate not in ["isDebug", "ModelCal", "VolumeCal", "BothMode"]):
                print("Wrong ModeString !")
                return False
            save = startSetUp[operate]
            booleanValue = not startSetUp[operate]
            startSetUp[operate] = int(booleanValue)

            print(f"{operate}: {bool(save)} ==>  {operate}: {bool(startSetUp[operate])}")
        with open(DebugBase.address, 'w') as f:
            f.write(json.dumps(startSetUp))
        return True

    def DebugTest(self, p):
        FileName = "TestProfile_" + p + ".txt"
        fileAddress = f'..\\..\\asset\\TestProfile\\{FileName}'
        if (platform.system().lower() != "windows"):
            fileAddress = f'..//..//asset//TestProfile//{FileName}'

        with open(fileAddress) as List:
            read = List.read()
            Data = eval(read)
        with open(DebugBase.address, 'r') as f:
            startSetUp = eval(f.read())
        print(Data)
        SectionDictObject = Data[0]
        HullListObject = Data[1]
        self.CDD = CanoeDataBase(SectionDictObject, HullListObject)
        self.DCCO = DataCalculation(self.CDD)

        # Actions base on Configuration
        # Test
        canoe = None
        if (bool(startSetUp["BothMode"])):
            self.MCCO = ModelCalculation(self.CDD)
            self.DCCO.CanoeDataCalculation()
            canoe = self.MCCO.Model_Generate()
            self.DCCO.CalDataReturn()
        elif (bool(startSetUp["ModelCal"])):
            self.MCCO = ModelCalculation(self.CDD)
            canoe = self.MCCO.Model_Generate()
        elif (bool(startSetUp["VolumeCal"])):
            self.DCCO.CanoeDataCalculation()
            self.DCCO.CalDataReturn()

        if ((bool(startSetUp["BothMode"])) or bool(startSetUp["ModelCal"])):
            # save file
            filename = "Test_Canoe.stl"
            filePath = "..\\..\\asset\\ModelFile\\" + filename
            saveProcess = Process(target=self.ConnectCanoeDateBase(filePath, canoe))
            saveProcess.start()
            saveProcess.join()
            # Wait Until Save

        print("SaveEnd")

    def ConnectCanoeDateBase(self, filePath, canoe):
        CanoeDataBase.SaveStlIntoFile_static(filePath, canoe)

    @staticmethod
    def ChangDebug(debugBoolean):
        with open(DebugBase.address, 'r') as f:
            startSetUp = eval(f.read())

        if (debugBoolean):
            digit = 1
        else:
            digit = 0

        startSetUp['isDebug'] = digit
        with open(DebugBase.address, 'w') as file_dict:
            file_dict.write(json.dumps(startSetUp))

    @staticmethod
    def restartProgram():
        sys.stdout.flush()
        actionList = ["python", "MainGUI.py"]
        os.execvp(actionList[0], actionList)


class HealthCheckBase():
    # TBD
    def __init__(self, ClassType):
        self.CT = ClassType

    def ErrorReturn(self, string):
        # return warning & error when wrong data input
        return 42

    def HCheck(self):
        # check the ability of program to run
        return 42
