import json
import os
import sys
from multiprocessing import Process

from CanoeDataBase import CanoeDataBase
from DataCalculation import DataCalculation
from ModelCalculation import ModelCalculation

# I learned how to use daemon from this guid:
#  https://www.geeksforgeeks.org/python-daemon-threads/
class DebugBase():
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
                        """)
            elif (Profile == 's'):
                print("enter Setting")
                self.configureSetting()

            elif (Profile not in ProfileList):
                Err = 'TestProfile not in the list'
                HealthCheckBase.ErrorReturn(Err)
            else:
                self.DebugTest(Profile)

            # End the Program
            print("Enter 'space' to end the program")
            Profile = input("Enter the TestProfile or 'space':")

    def configureSetting(self):
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'r') as f:
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
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'w') as f:
            f.write(json.dumps(startSetUp))
        return True


    def DebugTest(self, p):
        FileName = "TestProfile_" + p + ".txt"
        with open(f'..\\..\\asset\\TestProfile\\{FileName}') as List:
            read = List.read()
            Data = eval(read)
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'r') as f:
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

        if((bool(startSetUp["BothMode"])) or bool(startSetUp["ModelCal"])):
            # save file
            filename = "Test_Canoe.stl"
            filePath = "..\\..\\asset\\ModelFile\\" + filename
            saveProcess = Process(target = self.ConnectCanoeDateBase(filePath,canoe))
            saveProcess.start()
            saveProcess.join()
            # Wait Until Save

        print("SaveEnd")

    def ConnectCanoeDateBase(self,filePath,canoe):
        CanoeDataBase.SaveStlIntoFile_static(filePath,canoe)



    @staticmethod
    def ChangDebug(debugBoolean):
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'r') as f:
            startSetUp = eval(f.read())

        if (debugBoolean):
            digit = 1
        else:
            digit = 0

        startSetUp['isDebug'] = digit
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'w') as file_dict:
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
