import json
import os
import sys

from CanoeDataBase import CanoeDataBase
from DataCalculation import DataCalculation
from ModelCalculation import ModelCalculation


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
                Erro = 'TestProfile not in the list'
                HealthCheckBase.ErrorReturn(Erro)
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

    def config(self, modeString, startSetUp):
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
        with open(f'..\\..\\asset\\TestProfile\\{FileName}', 'w') as List:
            read = List.read()
            Data = eval(read)
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'r') as f:
            startSetUp = eval(f.read())

        SectionDictObject = Data[0]
        HullDictObject = Data[1]
        self.CDD = CanoeDataBase(SectionDictObject, HullDictObject)
        self.DCCO = DataCalculation(self.CDD)
        # Print out Current Data
        self.DCCO.CalDataReturn()
        # Actios base on Configuration
        # Test
        if (bool(startSetUp["ModelCal"]) and bool(startSetUp["VolumeCal"])):
            self.MCCO.Model_Generate()
            self.DCCO.Canoe_Volume()
            self.MCCO.Model_Generate()
        elif (bool(startSetUp["ModelCal"])):
            self.MCCO = ModelCalculation(self.CDD)
            self.MCCO.Model_Generate()
        elif (bool(startSetUp["VolumeCal"])):
            self.DCCO.Canoe_Volume()


    def ChangDebug(self, debugBoolean):
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'r') as f:
            startSetUp = eval(f.read())

        if (debugBoolean):
            digit = 1
        else:
            digit = 0

        startSetUp['isDebug'] = digit
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt', 'w') as file_dict:
            file_dict.write(json.dumps(startSetUp))

    def restartProgram(self):
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
