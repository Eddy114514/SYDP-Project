from CanoeDataBase import CanoeDataBase
from Calculation import Calculation
import sys ,os,json,time

class DebugBase():
    def __init__(self, debugBoolean):
        self.isDebug = debugBoolean

    def DebugMode(self,Profile):
        self.command_Read(Profile)
        End_Parameter = input("""End the debug mode? Enter: [y/n]""")

        if(End_Parameter == 'n'):
            print("Program End")
            sys.exit()
        elif(End_Parameter == 'y'): # exit the debug mode and restart
            print("Program End \n Debug Mode Off")
            self.ChangDebug(False)
            self.restartProgram()
        else:
            self.command_Read(Profile)

    def command_Read(self,Profile):
        ProfileList = ['sym', 'lsh', 'sch', 'ach', 'ath']
        while (Profile != " "):
            if (Profile not in ProfileList):
                HealthCheckBase.ErrorReturn('TestProfile not in the list')
            else:
                self.DebugTest(Profile)

            # End the Program
            print("Enter 'space' to end the program")
            Profile = input("Enter the TestProfile or 'space':")
            
    def DebugTest(self,p):
        FileName = "TestProfile_" + p + ".txt"
        with open(f'..\\..\\asset\\TestProfile\\{FileName}') as List:
            read = List.read()
            Data = eval(read)

        SectionDictObject = Data[0]
        HullDictObject = Data[1]
        self.CDD = CanoeDataBase(SectionDictObject, HullDictObject)
        self.CCO = Calculation(self.CDD)

        # Test
        self.CCO.CalDataReturn()
        self.CCO.Canoe_Volume()
        self.CCO.Model_Generate()

    def ChangDebug(self, debugBoolean):
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt','r') as f:
            startSetUp = eval(f.read())

        if(debugBoolean):
            digit = 1
        else:
            digit = 0

        startSetUp['isDebug'] = digit
        with open(f'..\\..\\asset\\startSetup\\setUpinformation.txt','w') as dict:
            dict.write(json.dumps(startSetUp))

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
