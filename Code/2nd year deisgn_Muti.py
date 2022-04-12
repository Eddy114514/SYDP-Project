import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import numpy as np
from decimal import Decimal
from sympy import *
import sympy
import math
from sympy import Pow
from sympy.plotting import plot3d
import pandas as pd
from pandastable import Table, TableModel
from tkinter import *
from tkinter.ttk import *
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
import mpmath as mp
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from numpy.random import randn
from scipy import array, newaxis
import multiprocessing as mup
from multiprocessing import *
import multiprocessing
import os
import signal
import time

##Set varibales for Math function processing
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')
a = sympy.Symbol('a')
b = sympy.Symbol('b')
c = sympy.Symbol('c')


class Canoedesignprogram(tk.Tk):
    ##Set the initial variables of canoe
    Canoe_Length = 0
    Canoe_width = 0
    Canoe_Depth = 0
    Canoe_Thickness = 0
    Canoe_Density = 0
    CrewWeight = 0
    Cover_Length = 0
    exponentFront = 0
    exponentWidth = 0
    exponentDepth = 0
    Thickness_Of_Cover = 0
    Canoe_data_dict = {}
    Canoe_data_Spreadsheet = {}
    Canoe_data_dict_light = {}
    #Creating the graphic user interface

    def __init__(self):
        super().__init__()

        self.title('Canoedesignprogram')
        """self.geometry("600x750")"""
        # configure the column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=3)

        self.createWidgets()

    def createWidgets(self):
        #Setting label for display, and type in text bar

        self.username_label = ttk.Label(
            self, text="Canoe Design Program", font=10)
        self.username_label.grid(column=1, row=1, sticky=tk.N,
                                 padx=10, pady=10, ipadx=5, ipady=5)

        self.Length_label = ttk.Label(self, text="Canoe Length :")
        self.Length_label.grid(
            column=0, row=3, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Length_entry = ttk.Entry(self)
        self.Length_entry.grid(column=1, row=3, sticky=tk.W, padx=10, pady=10)

        self.Width_label = ttk.Label(self, text="Canoe Width :")

        self.Width_label.grid(
            column=0, row=4, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Width_entry = ttk.Entry(self)
        self.Width_entry.grid(
            column=1, row=4, sticky=tk.W, padx=10, pady=10)

        self.Depth_label = ttk.Label(self, text="Canoe Depth :")
        self.Depth_label.grid(
            column=0, row=5, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Depth_entry = ttk.Entry(self)
        self.Depth_entry.grid(
            column=1, row=5, sticky=tk.W, padx=10, pady=10)

        self.Density_label = ttk.Label(self, text="Canoe Density :")
        self.Density_label.grid(
            column=0, row=6, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Density_entry = ttk.Entry(self)
        self.Density_entry.grid(
            column=1, row=6, sticky=tk.W, padx=10, pady=10)

        self.Thickness_label = ttk.Label(self, text="Canoe Thickness :")
        self.Thickness_label.grid(
            column=0, row=7, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Thickness_entry = ttk.Entry(self)
        self.Thickness_entry.grid(
            column=1, row=7, sticky=tk.W, padx=10, pady=10)

        self.ExponentCurve_label = ttk.Label(
            self, text="Exponent of Curve function :")
        self.ExponentCurve_label.grid(
            column=0, row=8, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.ExponentCurve_entry = ttk.Entry(self)
        self.ExponentCurve_entry.grid(
            column=1, row=8, sticky=tk.W, padx=10, pady=10)

        self.ExponentWidth_label = ttk.Label(
            self, text="Exponent of Width function :")
        self.ExponentWidth_label.grid(
            column=0, row=9, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.ExponentWidth_entry = ttk.Entry(self)
        self.ExponentWidth_entry.grid(
            column=1, row=9, sticky=tk.W, padx=10, pady=10)

        self.ExponentDepth_label = ttk.Label(
            self, text="Exponent of Depth function :")
        self.ExponentDepth_label.grid(
            column=0, row=10, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.ExponentDepth_entry = ttk.Entry(self)
        self.ExponentDepth_entry.grid(
            column=1, row=10, sticky=tk.W, padx=10, pady=10)

        self.Thicknesscover_label = ttk.Label(
            self, text="Thickness of Cover :")
        self.Thicknesscover_label.grid(
            column=0, row=11, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Thicknesscover_entry = ttk.Entry(self)
        self.Thicknesscover_entry.grid(
            column=1, row=11, sticky=tk.W, padx=10, pady=10)

        self.lengthcover_label = ttk.Label(self, text="Length of cover :")
        self.lengthcover_label.grid(
            column=0, row=12, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.lengthcover_entry = ttk.Entry(self)
        self.lengthcover_entry.grid(
            column=1, row=12, sticky=tk.W, padx=10, pady=10)

        self.Crewweight_label = ttk.Label(self, text="Weight of Crew :")
        self.Crewweight_label.grid(
            column=0, row=13, sticky=tk.E, padx=10, pady=10, ipadx=5, ipady=5)
        self.Crewweight_entry = ttk.Entry(self)
        self.Crewweight_entry.grid(
            column=1, row=13, sticky=tk.W, padx=10, pady=10)

        # Configure bottons
        self.Instruction = ttk.Button(self, text="Need Help?")
        self.Instruction.grid(
            column=2, row=2, sticky=tk.N, padx=10, pady=10, ipadx=10, ipady=10)
        self.Instruction.bind("<Button>", lambda e: Insturctionwindow())

        self.Instruction = ttk.Button(
            self, text="Input Data", command=self.returnTomain)
        self.Instruction.grid(
            column=3, row=2, sticky=tk.N, padx=10, pady=10, ipadx=10, ipady=10)

        self.Instruction = ttk.Button(
            self, text="Creat 3D Model", command=self.Datapointprint)
        self.Instruction.grid(
            column=2, row=3, sticky=tk.N, padx=10, pady=10, ipadx=10, ipady=10)

        self.Data = ttk.Button(
            self, text="Show DataFrame")
        self.Data.grid(
            column=3, row=3, sticky=tk.N, padx=10, pady=10, ipadx=10, ipady=10)
        self.Data.bind("<Button>", lambda e: Dataframewindow(self))

        self.Calculation = ttk.Button(
            self, text="Cal Data", command=self.calculation)
        self.Calculation.grid(
            column=0, row=14, sticky=tk.N, padx=10, pady=10, ipadx=5, ipady=5)

        self.Freeboard = ttk.Button(self, text="Cal Freeboard")
        self.Freeboard.grid(
            column=1, row=14, sticky=tk.W, padx=10, pady=1, ipadx=5, ipady=5)

        self.Draw = ttk.Button(self, text="Graph Canoe",
                               command=self.DrawCanoe)
        self.Draw.grid(
            column=2, row=14, sticky=tk.W, padx=10, pady=10, ipadx=5, ipady=5)

        self.Findbest = ttk.Button(
            self, text="Find Best result", command=self.Findbest)
        self.Findbest.grid(
            column=3, row=14, sticky=tk.N, padx=10, pady=10, ipadx=5, ipady=5)

    def returnTomain(self):
        #Get the data that user type in from the GUI, and sign in them to the Global variable.
        Canoedesignprogram.Canoe_Length = float(self.Length_entry.get())
        Canoedesignprogram.Canoe_width = float(self.Width_entry.get())
        Canoedesignprogram.Canoe_Depth = float(self.Depth_entry.get())
        Canoedesignprogram.Canoe_Thickness = float(self.Thickness_entry.get())
        Canoedesignprogram.Canoe_Density = float(self.Density_entry.get())
        Canoedesignprogram.CrewWeight = float(self.Crewweight_entry.get())
        Canoedesignprogram.Cover_Length = float(self.lengthcover_entry.get())
        Canoedesignprogram.exponentFront = float(
            self.ExponentCurve_entry.get())
        Canoedesignprogram.exponentWidth = float(
            self.ExponentWidth_entry.get())
        Canoedesignprogram.exponentDepth = float(
            self.ExponentDepth_entry.get())
        Canoedesignprogram.Thickness_Of_Cover = float(
            self.Thicknesscover_entry.get())

        # Test
        print("length", Canoedesignprogram.Canoe_Length)
        print("width", Canoedesignprogram.Canoe_width)
        print("depth", Canoedesignprogram.Canoe_Depth)
        print("thickness", Canoedesignprogram.Canoe_Thickness)
        print("canoe_density", Canoedesignprogram.Canoe_Density)
        print("crewweight", Canoedesignprogram.CrewWeight)
        print("coverlength", Canoedesignprogram.Cover_Length)
        print("expoenntfront", Canoedesignprogram.exponentFront)
        print("exponentwidth", Canoedesignprogram.exponentWidth)
        print("exponentdepth", Canoedesignprogram.exponentDepth)
        print("thickenss of cover", Canoedesignprogram.Thickness_Of_Cover)

    def calculation(self):
        #Calculate Canoe's details through calcuse application and function processing.
        Canoe_displacement, Concrete_displacement, Volume_styrofoam, Submerge_displacement = self.calvolume()
        Canoe_Buoyancy, Canoe_Capability, Submerge_Buoyancy, Submerge_Capability = self.calbuoyancy(
            Canoe_displacement, Submerge_displacement)
        Canoe_Weight, Canoe_and_crew_weight = self.calweight(
            Concrete_displacement)
        Pass_Submerge = False
        Pass_Flow_with_crew = False
        if(Submerge_Capability > Canoe_Weight):
            Pass_Submerge = True
        if(Canoe_Capability > Canoe_and_crew_weight):
            Pass_Flow_with_crew = True

        # Set dict
        unit1 = "Lbs"
        unit2 = "Cubic Inch"
        Unit3 = "N"
        #Creating the dict.
        Canoedesignprogram.Canoe_data_dict = \
            {"Canoe_displacement": [Canoe_displacement, unit2],
             "Concrete_displacement": [Concrete_displacement, unit2],
             "Volume_styrofoam": [Volume_styrofoam, unit2],
             "Submerge_displacement": [Submerge_displacement, unit2],
             "Canoe_Buoyancy": [Canoe_Buoyancy, Unit3],
             "Canoe_Capability": [Canoe_Capability, unit1],
             "Submerge_Buoyancy": [Submerge_Buoyancy, Unit3],
             "Submerge_Capability": [Submerge_Capability, unit1],
             "Canoe_Weight": [Canoe_Weight, unit1],
             "Canoe_and_crew_weight": [Canoe_and_crew_weight, unit1],
             "Pass_Submerge": [Pass_Submerge, "Boolean"],
             "Pass_Flow_with_crew": [Pass_Flow_with_crew, "Boolean"]
             }

        # Change dict to spread sheet form
        Canoe_data_Spreadsheet_Show = pd.DataFrame.from_dict(
            Canoedesignprogram.Canoe_data_dict, orient='index')
        Canoedesignprogram.Canoe_data_Spreadsheet = pd.DataFrame.from_dict(
            Canoedesignprogram.Canoe_data_dict)
        # test
        print(Canoe_data_Spreadsheet_Show)
        print(Canoedesignprogram.Canoe_data_Spreadsheet)
        print(Canoedesignprogram.Canoe_data_dict)
        # Show the spread sheet

    def Calculation_light(self, rank):
        #previous "Calculation" require many memory, not efficent for massive simulation, so reduce it to more simple form
        Canoe_displacement, Concrete_displacement, Volume_styrofoam, Submerge_displacement = self.calvolume()
        Canoe_Buoyancy, Canoe_Capability, Submerge_Buoyancy, Submerge_Capability = self.calbuoyancy(
            Canoe_displacement, Submerge_displacement)
        Canoe_Weight, Canoe_and_crew_weight = self.calweight(
            Concrete_displacement)
        Pass_Submerge = False
        Pass_Flow_with_crew = False
        if(Submerge_Capability > Canoe_Weight):
            Pass_Submerge = True
        if(Canoe_Capability > Canoe_and_crew_weight):
            Pass_Flow_with_crew = True

        Datasave_dict = \
            {
             "Rank": str(rank),
             "ExponentFront": Canoedesignprogram.exponentFront,
             "ExponentWidth": Canoedesignprogram.exponentWidth,
             "ExponentDepth": Canoedesignprogram.exponentDepth,
             "Canoe_displacement": Canoe_displacement,
             "Concrete_displacement": Concrete_displacement,
             "Volume_styrofoam": Volume_styrofoam,
             "Submerge_displacement": Submerge_displacement,
             "Canoe_Buoyancy": Canoe_Buoyancy,
             "Canoe_Capability": Canoe_Capability,
             "Submerge_Buoyancy": Submerge_Buoyancy,
             "Submerge_Capability": Submerge_Capability,
             "Canoe_Weight": Canoe_Weight,
             "Canoe_and_crew_weight": Canoe_and_crew_weight,
             "Pass_Submerge": Pass_Submerge,
             "Pass_Flow_with_crew": Pass_Flow_with_crew
             }
        Dict_to_list = list(Datasave_dict.values())

        Canoedesignprogram.Canoe_data_dict_light[str(rank)] = Dict_to_list

    def calbuoyancy(self, Canoe_displacement, Submerge_displacement):
        g = 9.8
        densityofwater = 997
        Canoe_Buoyancy = (Canoe_displacement/61024)*g*densityofwater
        Canoe_Capability = (Canoe_Buoyancy/g)*2.205

        Submerge_Buoyancy = (
            (Submerge_displacement)/61024)*g*densityofwater
        Submerge_Capability = (Submerge_Buoyancy/g)*2.205

        # test
        print("Canoe_Buoyancy", Canoe_Buoyancy)
        print("Canoe_Capability", Canoe_Capability)
        print("Submerge_Buoyancy", Submerge_Buoyancy)
        print("Submerge_Capability", Submerge_Capability)

        return(Canoe_Buoyancy, Canoe_Capability, Submerge_Buoyancy, Submerge_Capability)

    def calweight(self, Concrete_displacement):
        Concrete_displacement_feet = Concrete_displacement/1728
        Canoe_weight = Concrete_displacement_feet * \
            Canoedesignprogram.Canoe_Density
        Canoe_and_crew_weight = Canoe_weight+Canoedesignprogram.CrewWeight

        # test
        print("Canoe_weight", Canoe_weight)
        print("Canoe_and_crew_weight", Canoe_and_crew_weight)

        return(Canoe_weight, Canoe_and_crew_weight)

    def calvolume(self):
        Canoe_width_semi = Canoedesignprogram.Canoe_width/2
        Canoe_length_semi = Canoedesignprogram.Canoe_Length/2

        # Configure Function

        swfunction = Canoe_width_semi * \
            (x/Canoe_length_semi)**Canoedesignprogram.exponentWidth

        dfunction = Canoedesignprogram.Canoe_Depth * \
            (x/Canoe_length_semi)**Canoedesignprogram.exponentDepth

        swfunctionout = (Canoe_width_semi+Canoedesignprogram.Canoe_Thickness) * \
            (x/(Canoe_length_semi+Canoedesignprogram.Canoe_Thickness)
             )**Canoedesignprogram.exponentWidth

        dfunctionout = (Canoedesignprogram.Canoe_Depth+Canoedesignprogram.Canoe_Thickness) * \
            (x/(Canoe_length_semi+Canoedesignprogram.Canoe_Thickness)
             )**Canoedesignprogram.exponentDepth

        Volume_Function_Inside = 2*2*((Canoedesignprogram.exponentFront)/(Canoedesignprogram.exponentFront+1)) * \
            integrate(swfunction*dfunction,
                      (x, 0, Canoe_length_semi))

        Volume_Function_Outside = 2*2*((Canoedesignprogram.exponentFront)/(Canoedesignprogram.exponentFront+1)) * \
            integrate(swfunctionout*dfunctionout,
                      (x, 0, Canoe_length_semi+Canoedesignprogram.Canoe_Thickness))

        Volume_styrofoam = 2*2*((Canoedesignprogram.exponentFront)/(Canoedesignprogram.exponentFront+1)) * \
            integrate(swfunction*dfunction,
                      (x, 0, Canoedesignprogram.Cover_Length+Canoedesignprogram.Canoe_Thickness))

        Volume_cover_horizontal = Canoedesignprogram.Thickness_Of_Cover*2*2 * integrate(swfunction, (x, 0, Canoedesignprogram.Cover_Length
                                                                                                     + Canoedesignprogram.Canoe_Thickness))
        Canoe_displacement = Volume_Function_Outside

        Concrete_displacement = Volume_Function_Outside - \
            Volume_Function_Inside+Volume_cover_horizontal

        Submerge_displacement = Volume_styrofoam+Concrete_displacement

        # test
        print("Compare", Volume_Function_Inside)
        print("Canoe_displacement", Canoe_displacement)
        print("Concrete_displacement", Concrete_displacement)
        print("Volume_styrofoam", Volume_styrofoam)
        print("Submerge_displacement", Submerge_displacement)

        return(Canoe_displacement, Concrete_displacement, Volume_styrofoam, Submerge_displacement)

    def DrawCanoe(self):
        #Drawcanoe provide a brife view of the canoe, base on its side view.

        Canoe_width_semi = Canoedesignprogram.Canoe_width/2
        Canoe_length_semi = Canoedesignprogram.Canoe_Length/2

        Canoe_width_fucntion = (Canoe_width_semi+Canoedesignprogram.Canoe_Thickness) * \
            (x/(Canoe_length_semi
                + Canoedesignprogram.Canoe_Thickness))**Canoedesignprogram.exponentWidth

        Canoe_width_function_inside = Canoe_width_semi * \
            (x/Canoe_length_semi)**Canoedesignprogram.exponentWidth
        #Neg mean negative, the middle point of the canoe is 0, its left is negative, its right is positive.
        Canoe_width_function_neg = -1*(Canoe_width_semi+Canoedesignprogram.Canoe_Thickness) * \
            (x/(Canoe_length_semi + Canoedesignprogram.Canoe_Thickness)
             )**Canoedesignprogram.exponentWidth

        Canoe_width_function_inside_neg = -1*(Canoe_width_semi
                                              * (x/Canoe_length_semi)**Canoedesignprogram.exponentWidth)

        Canoe_depth_function = -1*(Canoedesignprogram.Canoe_Depth+Canoedesignprogram.Canoe_Thickness) * \
            (x/(Canoe_length_semi+Canoedesignprogram.Canoe_Thickness)
             )**Canoedesignprogram.exponentDepth

        Canoe_depth_function_inside = -1 * \
            (Canoedesignprogram.Canoe_Depth * (x/Canoe_length_semi)
             ** Canoedesignprogram.exponentDepth)

        Canoe_curve_function_inside = (Canoedesignprogram.Canoe_Depth*x**Canoedesignprogram.exponentFront)/(
            Canoe_width_semi**Canoedesignprogram.exponentFront)

        plot(Canoe_width_fucntion, Canoe_width_function_neg,
             Canoe_depth_function, Canoe_width_function_inside,
             Canoe_width_function_inside_neg,
             Canoe_depth_function_inside, (x, 0, Canoe_length_semi))

        plot(Canoe_curve_function_inside, -1*Canoe_curve_function_inside,
             xlim=[-1*Canoe_width_semi, Canoe_width_semi], ylim=[0, Canoedesignprogram.Canoe_Depth])

        """# Get funcion list

        Function_list=[]

        swfunction = Canoe_width_semi * (x/Canoe_length_semi)**Canoedesignprogram.exponentWidth

        dfunction = Canoedesignprogram.Canoe_Depth *(x/Canoe_length_semi)**Canoedesignprogram.exponentDepth

        Depth_at_point = 0
        SW_at_point = 0
        Datapointdistance=4
        Canoe_curve_function_inside = (Depth_at_point*x**Canoedesignprogram.exponentFront)/(SW_at_point**Canoedesignprogram.exponentFront)
        for point in np.arange(Datapointdistance, Canoe_length_semi+1, Datapointdistance):
            Depth_at_point = dfunction.subs(x, point)
            SW_at_point = swfunction.subs(x, point)
            Canoe_curve_function_inside = (Depth_at_point*x**Canoedesignprogram.exponentFront)/(SW_at_point**Canoedesignprogram.exponentFront)
            Canoe_curve_function_inside_Neg=-1*(Depth_at_point*x**Canoedesignprogram.exponentFront)/(SW_at_point**Canoedesignprogram.exponentFront)
            plot(Canoe_curve_function_inside,Canoe_curve_function_inside_Neg,(x,-1*Canoe_length_semi,Canoe_length_semi))"""

    def Findbest(self):
        # The range of exponent_curve will be from 3 to 7 [3,7]
        # The range of exponent_width will be from 0.05 to 1 [0.05,1]
        # The range of exponent_depth will be from 0.05 to 1 [0.05,1]

        #ExpDict Save
        Exponent_Dict = {}

        #MUTIfunction dicts
        Out_Volume_Dict = {}
        Inside_Volume_Dict = {}
        Cover_Volume_Dict = {}
        Styrofoam_Volume_Dict = {}

        #Weight and buoyancy dicts
        Concrete_Weight_Dict = {}
        Submerge_Dict = {}
        Capability_Dict = {}

        #Comparedicts
        BuoyancyCheck_Dict = {}
        SubmergeCheck_Dict = {}

        #Final dict
        Final_Pass_Dict = {}

        Canoedesignprogram.exponentFront = 3
        expc = 3
        Canoedesignprogram.exponentWidth = 0.05
        expw = 0.05
        Canoedesignprogram.exponentDepth = 0.05
        expd = 0.05
        # For test
        count = 0
        # Save explist of all

        #For save time transform total vari to locals
        Variables_Canoe = [(Canoedesignprogram.Canoe_width/2), (Canoedesignprogram.Canoe_Length/2),
                           Canoedesignprogram.Canoe_Depth, Canoedesignprogram.Cover_Length, Canoedesignprogram.Canoe_Thickness]

        print(Variables_Canoe)

        for expc in np.arange(3, 7.25, 0.25):
            expc = round(expc, 3)
            Canoedesignprogram.exponentFront = expc
            for expw in np.arange(0.25, 1.25, 0.25):
                expw = round(expw, 3)
                Canoedesignprogram.exponentWidth = expw
                for expd in np.arange(0.25, 1.25, 0.25):
                    expd = round(expd, 3)
                    Canoedesignprogram.exponentDepth = expd

                    Exponent_Dict[count] = [
                        expc, expw, expd]
                    count += 1

                    print("Creating Format ", count)
        if __name__ == "__main__":

            num_cores = int(mup.cpu_count())
            time.sleep(1)
            print("The Computer Have: " + str(num_cores)
                  + " Central Processing Units")

            InsideV_Q = mup.Queue()
            OutsideV_Q = mup.Queue()
            CoverV_Q = mup.Queue()
            StyrofoamV_Q = mup.Queue()
            pool_first = multiprocessing.Pool(processes=num_cores)
            for CountnumberF, EXPlist in Exponent_Dict.items():

                pool_first.apply_async(self.InsideV_Cal(
                    CountnumberF, InsideV_Q, EXPlist, Variables_Canoe))
                pool_first.apply_async(self.OutsideV_Cal(
                    CountnumberF, OutsideV_Q, EXPlist, Variables_Canoe))
                pool_first.apply_async(self.CoverV_Cal(
                    CountnumberF, CoverV_Q, EXPlist, Variables_Canoe))
                pool_first.apply_async(self.Styrofoam_Cal(
                    CountnumberF, StyrofoamV_Q, EXPlist, Variables_Canoe))

                Inside_Volume_Dict[CountnumberF] = InsideV_Q.get()
                Out_Volume_Dict[CountnumberF] = OutsideV_Q.get()
                Cover_Volume_Dict[CountnumberF] = CoverV_Q.get()
                Styrofoam_Volume_Dict[CountnumberF] = StyrofoamV_Q.get()

            pool_first.close()
            pool_first.join()

            pool_sec = multiprocessing.Pool(processes=num_cores)

            Capability_Q = mup.Queue()
            ConcreteW_Q = mup.Queue()
            Submerge_Q = mup.Queue()

            for CountnumberS, EXPlist in Exponent_Dict.items():

                pool_sec.apply_async(self.Capability_Cal(
                    Out_Volume_Dict, Capability_Q, CountnumberS))
                pool_sec.apply_async(self.ConcreteW_Cal(
                    Out_Volume_Dict, Inside_Volume_Dict, Cover_Volume_Dict, ConcreteW_Q, CountnumberS))
                pool_sec.apply_async(self.Submerge_Cal(
                    Out_Volume_Dict, Inside_Volume_Dict, Cover_Volume_Dict, Styrofoam_Volume_Dict, Submerge_Q, CountnumberS))

                Capability_Dict[CountnumberS] = Capability_Q.get()
                Concrete_Weight_Dict[CountnumberS] = ConcreteW_Q.get()
                Submerge_Dict[CountnumberS] = Submerge_Q.get()

            pool_sec.close()
            pool_sec.join()

            pool_third = multiprocessing.Pool(processes=num_cores)

            BuoyancyCheck_Q = mup.Queue()
            SubmergeCheck_Q = mup.Queue()

            Creweight_Sent = Canoedesignprogram.CrewWeight

            for CounternumberT, weight in Concrete_Weight_Dict.items():
                pool_third.apply_async(self.Canflow_Compare(
                    BuoyancyCheck_Q, Capability_Dict, Concrete_Weight_Dict, Creweight_Sent, CounternumberT))
                pool_third.apply_async(self.CanSubmerge_Compare(
                    SubmergeCheck_Q, Submerge_Dict, Concrete_Weight_Dict, CounternumberT))

                BuoyancyCheck_Dict[CounternumberT] = BuoyancyCheck_Q.get()
                SubmergeCheck_Dict[CounternumberT] = SubmergeCheck_Q.get()

            pool_third.close()
            pool_third.join()
            Weight_Compare_Dist = {}

            for CountnumberFOUR in BuoyancyCheck_Dict.keys():

                if(BuoyancyCheck_Dict[CountnumberFOUR] == 1 and SubmergeCheck_Dict[CountnumberFOUR] == 1):
                    Final_Pass_Dict[CountnumberFOUR] = Exponent_Dict[CountnumberFOUR]
                    Weight_Compare_Dist[CountnumberFOUR] = Concrete_Weight_Dict[CountnumberFOUR]
                    print("Finding Pass Canoes : ", CountnumberFOUR)

            print(Weight_Compare_Dist)

            Weight_Compare_List = sorted(Weight_Compare_Dist.items(
            ), key=lambda Weight_Compare_Dist: (Weight_Compare_Dist[1]))

            print(Weight_Compare_List)

            Countnum = 1
            Top10Dict = {}
            for CountforTop10 in Weight_Compare_List:
                if(Countnum <= 10):
                    print(CountforTop10[0])
                    Top10Dict[CountforTop10[0]
                              ] = Final_Pass_Dict[CountforTop10[0]]
                    Countnum += 1

            Top_10_dataframe = pd.DataFrame.from_dict(
                Top10Dict, orient='index')
            print(Top_10_dataframe)

            Countnum_secound = 1

            Canoedesignprogram.Canoe_data_dict_light["Category"] = ["Rank", "ExponentFront", "ExponentWidth", "ExponentDepth",
                                                                    "Canoe_displacement", "Concrete_displacement",
                                                                    "Volume_styrofoam", "Submerge_displacement", "Canoe_Buoyancy",
                                                                    "Canoe_Capability", "Submerge_Buoyancy", "Submerge_Capability", "Canoe_Weight",
                                                                    "Canoe_and_crew_weight", "Pass_Submerge", "Pass_Flow_with_crew"]

            for CountnumberFIF in Top10Dict.values():
                expc = CountnumberFIF[0]
                expw = CountnumberFIF[1]
                expd = CountnumberFIF[2]

                Canoedesignprogram.exponentFront = expc
                Canoedesignprogram.exponentWidth = expw
                Canoedesignprogram.exponentDepth = expd

                self.Calculation_light(Countnum_secound)

                Countnum_secound += 1

            print(Canoedesignprogram.Canoe_data_dict_light)

            Messagebox_answer = tkinter.messagebox.askokcancel(
                title="Show or not?", message="Want show the top 10 Canoe data?")
            if(Messagebox_answer == True):
                Canoedesignprogram.Canoe_data_Spreadsheet = pd.DataFrame.from_dict(
                    Canoedesignprogram.Canoe_data_dict_light)
                print(Canoedesignprogram.Canoe_data_Spreadsheet)

                Dataframewindow(self)

            if(Messagebox_answer == False):
                Canoedesignprogram.Canoe_data_Spreadsheet = pd.DataFrame.from_dict(
                    Canoedesignprogram.Canoe_data_dict_light)

                print(Canoedesignprogram.Canoe_data_Spreadsheet)

    def Canflow_Compare(self, BuoyancyCheck_Q, Capability_Dict, Concrete_Weight_Dict, Creweight_Sent, CounternumberT):

        if(Capability_Dict[CounternumberT] > Concrete_Weight_Dict[CounternumberT]+Creweight_Sent):
            BuoyancyCheck_Q.put(1)

        elif(Capability_Dict[CounternumberT] <= Concrete_Weight_Dict[CounternumberT]+Creweight_Sent):
            BuoyancyCheck_Q.put(0)

        print("Checking Buoyancy : ", CounternumberT)

    def CanSubmerge_Compare(self, SubmergeCheck_Q, Submerge_Dict, Concrete_Weight_Dict, CounternumberT):

        if(Submerge_Dict[CounternumberT] > Concrete_Weight_Dict[CounternumberT]):
            SubmergeCheck_Q.put(1)

        elif(Submerge_Dict[CounternumberT] <= Concrete_Weight_Dict[CounternumberT]):
            SubmergeCheck_Q.put(0)

        print("Checking Submerge : ", CounternumberT)

    def Submerge_Cal(self, OVDict, IVDict, CVDict, SVDict, Submerge_Q, Countnumber):
        volume = OVDict[Countnumber]-IVDict[Countnumber] + \
            CVDict[Countnumber]+SVDict[Countnumber]
        densityofwater = 997
        print("Calculating Submerge   : ", Countnumber)
        Submerge_Q.put((volume/61024)*densityofwater*2.205)

    def Capability_Cal(self, OutVdict, Capability_Q, Countnumber):
        densityofwater = 997
        print("Calculating Capability : ", Countnumber)
        Capability_Q.put((OutVdict[Countnumber]/61024)*densityofwater*2.205)

    def ConcreteW_Cal(self, OutVdict, InVdict, CVdict, ConcreteW_Q, Countnumber):
        print("Calculating Weight     : ", Countnumber)
        Weight_Canoe = ((OutVdict[Countnumber]-InVdict[Countnumber]
                         + CVdict[Countnumber])/1728)*Canoedesignprogram.Canoe_Density
        ConcreteW_Q.put(Weight_Canoe)

    def Styrofoam_Cal(self, Countnumber, StyrofoamV_Q, EXPlist, Variables_Canoe):

        Canoe_width_semi = Variables_Canoe[0]
        Canoe_length_semi = Variables_Canoe[1]
        Canoe_Depth = Variables_Canoe[2]
        Cover_Length = Variables_Canoe[3]
        Canoe_Thickness = Variables_Canoe[4]

        expc = EXPlist[0]
        expw = EXPlist[1]
        expd = EXPlist[2]

        swfunction = Canoe_width_semi*(x/Canoe_length_semi)**expw

        dfunction = Canoe_Depth * \
            (x/Canoe_length_semi)**expd

        Volume_styrofoam = 2*2*((expc)/(expc+1))*integrate(swfunction*dfunction,
                                                           (x, 0, Cover_Length+Canoe_Thickness))

        print("Calculating Styrofoam Volume : ", Countnumber)

        StyrofoamV_Q.put(Volume_styrofoam)

    def OutsideV_Cal(self, Countnumber, OutsideV_Q, EXPlist, Variables_Canoe):

        expc = EXPlist[0]
        expw = EXPlist[1]
        expd = EXPlist[2]

        Canoe_width_semi = Variables_Canoe[0]
        Canoe_length_semi = Variables_Canoe[1]
        Canoe_Depth = Variables_Canoe[2]
        Cover_Length = Variables_Canoe[3]
        Canoe_Thickness = Variables_Canoe[4]

        swfunctionout = (Canoe_width_semi+Canoe_Thickness) * (
            x/(Canoe_length_semi+Canoe_Thickness))**expw

        dfunctionout = (Canoe_Depth+Canoe_Thickness) * \
            (x/(Canoe_length_semi+Canoe_Thickness)
             )**expd

        Volume_Function_Outside = 2*2*((expc)/(expc+1)) * \
            integrate(swfunctionout*dfunctionout,
                      (x, 0, Canoe_length_semi+Canoe_Thickness))

        print("Calculating Outside Volume : ", Countnumber)

        OutsideV_Q.put(Volume_Function_Outside)

    def InsideV_Cal(self, Countnumber, InsideV_Q, EXPlist, Variables_Canoe):

        Canoe_width_semi = Variables_Canoe[0]
        Canoe_length_semi = Variables_Canoe[1]
        Canoe_Depth = Variables_Canoe[2]
        Cover_Length = Variables_Canoe[3]
        Canoe_Thickness = Variables_Canoe[4]

        expc = EXPlist[0]
        expw = EXPlist[1]
        expd = EXPlist[2]

        swfunction = Canoe_width_semi * (x/Canoe_length_semi)**expw

        dfunction = Canoe_Depth * \
            (x/Canoe_length_semi)**expd

        Volume_Function_Inside = 2*2 * \
            ((expc)/(expc+1)) * integrate(swfunction
                                          * dfunction, (x, 0, Canoe_length_semi))

        print("Calculating Inside Volume : ", Countnumber)

        InsideV_Q.put(Volume_Function_Inside)

    def CoverV_Cal(self, Countnumber, CoverV_Q, EXPlist, Variables_Canoe):

        Canoe_width_semi = Variables_Canoe[0]
        Canoe_length_semi = Variables_Canoe[1]
        Canoe_Depth = Variables_Canoe[2]
        Cover_Length = Variables_Canoe[3]
        Canoe_Thickness = Variables_Canoe[4]

        expw = EXPlist[1]

        swfunction = Canoe_width_semi * (x/Canoe_length_semi)**expw

        Volume_cover_horizontal = Canoe_Thickness*2*2 * \
            integrate(swfunction, (x, 0, Cover_Length
                                   + Canoe_Thickness))

        print("Calculating Cover Volume : ", Countnumber)

        CoverV_Q.put(Volume_cover_horizontal)

    def Datapointprint(self):
        #Datapointprint is a complex method,first, it print calculate coordniate point of canoe from X,Y,Z and save them.
        #Them sign them into the Matplotlib with a point connect method and then format a surface, and it is 3D.

        # Value of datapoint distance
        Datapointdistance = 4

        # Set Original Zero Point
        XCoordinatelist_3D = []
        YCoordinatelist_3D = []
        ZCoordinatelist_3D = []
        Depthpluspoint = 0.0+Canoedesignprogram.Canoe_Depth
        Lengthpluspoint = Canoedesignprogram.Canoe_Length
        XCoordinatelist_3D.append(float(0.0))
        YCoordinatelist_3D.append(float(Depthpluspoint))
        ZCoordinatelist_3D.append(float(0.0))

        Canoe_width_semi = Canoedesignprogram.Canoe_width/2
        Canoe_length_semi = Canoedesignprogram.Canoe_Length/2

        # Prepare for creating fucntions

        swfunction = Canoe_width_semi * \
            (x/Canoe_length_semi)**Canoedesignprogram.exponentWidth

        dfunction = Canoedesignprogram.Canoe_Depth * \
            (x/Canoe_length_semi)**Canoedesignprogram.exponentDepth

        Depth_at_point = 0
        SW_at_point = 0
        Canoe_curve_function_inside = (
            Depth_at_point*x**Canoedesignprogram.exponentFront)/(SW_at_point**Canoedesignprogram.exponentFront)
        print(Canoedesignprogram.Cover_Length)
        for point in np.arange(Datapointdistance, Canoe_length_semi+1, Datapointdistance):
            Depth_at_point = dfunction.subs(x, point)
            SW_at_point = swfunction.subs(x, point)
            Canoe_curve_function_inside = (
                Depth_at_point*x**Canoedesignprogram.exponentFront)/(SW_at_point**Canoedesignprogram.exponentFront)

            print(point, " inch : ", Canoe_curve_function_inside)
            XCoordinatelist_3D_Get, YCoordinatelist_3D_Get, ZCoordinatelist_3D_Get = self.PrintCoordinate(
                Canoe_curve_function_inside, SW_at_point, point)
            XCoordinatelist_3D.extend(XCoordinatelist_3D_Get)
            YCoordinatelist_3D.extend(YCoordinatelist_3D_Get)
            ZCoordinatelist_3D.extend(ZCoordinatelist_3D_Get)

        Messagebox_answer = tkinter.messagebox.askokcancel(
            title="Half or Full?", message="Want to Generate Half of Canoe? (Warning! No means draw Full canoe)")
        if(Messagebox_answer == True):
            self.Draw3dmodel(XCoordinatelist_3D,
                             YCoordinatelist_3D, ZCoordinatelist_3D)

        if(Messagebox_answer == False):
            Outside_count = Canoe_length_semi+Datapointdistance

            for point_another in np.arange(Canoe_length_semi-Datapointdistance, 0, -1*Datapointdistance):
                Depth_at_point = dfunction.subs(x, point_another)
                SW_at_point = swfunction.subs(x, point_another)
                Canoe_curve_function_inside = (
                    Depth_at_point*x**Canoedesignprogram.exponentFront)/(SW_at_point**Canoedesignprogram.exponentFront)

                print(Outside_count, " inch : ", Canoe_curve_function_inside)
                XCoordinatelist_3D_Get_Another, YCoordinatelist_3D_Get_Another, ZCoordinatelist_3D_Get_Another = self.PrintCoordinate(
                    Canoe_curve_function_inside, SW_at_point, Outside_count)
                XCoordinatelist_3D = XCoordinatelist_3D+XCoordinatelist_3D_Get_Another
                YCoordinatelist_3D = YCoordinatelist_3D+YCoordinatelist_3D_Get_Another
                ZCoordinatelist_3D = ZCoordinatelist_3D+ZCoordinatelist_3D_Get_Another
                Outside_count += Datapointdistance

            XCoordinatelist_3D.append(float(0.0))
            YCoordinatelist_3D.append(float(Depthpluspoint))
            ZCoordinatelist_3D.append(float(Lengthpluspoint))

            print(XCoordinatelist_3D)
            print(YCoordinatelist_3D)
            print(ZCoordinatelist_3D)

            self.Draw3dmodel(XCoordinatelist_3D,
                             YCoordinatelist_3D, ZCoordinatelist_3D)

    def Draw3dmodel(self, XList, YList, ZList):

        fig = plt.figure()
        fig.set_size_inches(10.5, 10.5)
        ax = fig.add_subplot(projection='3d')

        ax.plot_trisurf(XList, ZList, YList, cmap=cm.jet, linewidth=0)

        ax.set_xlabel('Width')
        ax.set_ylabel('Length')
        ax.set_zlabel('Depth')

        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(6))
        ax.zaxis.set_major_locator(MaxNLocator(5))

        fig.tight_layout()

        world_limits = ax.get_w_lims()
        ax.set_box_aspect((world_limits[1]-world_limits[0], world_limits[3]
                           - world_limits[2], world_limits[5]-world_limits[4]))

        plt.show()

    def PrintCoordinate(self, Canoe_curve_function_inside, semilength, Point):
        XCoordinatelist = []
        YCoordinatelist = []

        XCoordinatelist_3D = []
        YCoordinatelist_3D = []
        ZCoordinatelist_3D = []

        Coordniatedict = {"X-value": XCoordinatelist,
                          "Y-value": YCoordinatelist}
        steps = semilength/0.5
        intsteps = int(steps)+1

        Final_Coordinate = Canoe_curve_function_inside.subs(x, semilength)

        Height_for_flat_surface = Canoedesignprogram.Canoe_Depth-Final_Coordinate

        Height_for_flat_surface = round(Height_for_flat_surface, 6)

        for Steps in range(0, intsteps):
            XCoordinate = Steps*0.5
            YCoordinate = Canoe_curve_function_inside.subs(x, XCoordinate)
            YCoordinate = round(YCoordinate, 4)
            Coordniatedict["X-value"].append(float(XCoordinate))
            Coordniatedict["Y-value"].append(float(YCoordinate))
            # Set 3d TableModel
            XCoordinatelist_3D.append(float(XCoordinate))
            YCoordinatelist_3D.append(
                float(YCoordinate+Height_for_flat_surface))
            ZCoordinatelist_3D.append(float(Point))

        Final_Coordinate = round(Final_Coordinate, 4)
        Coordniatedict["X-value"].append(semilength)
        Coordniatedict["Y-value"].append(Final_Coordinate)

        XCoordinatelist_3D.append(float(semilength))
        YCoordinatelist_3D.append(
            float(Final_Coordinate+Height_for_flat_surface))
        ZCoordinatelist_3D.append(float(Point))

        # Connect
        XCoordinatelist_3D.append(float(-1*semilength))
        YCoordinatelist_3D.append(
            float(Final_Coordinate+Height_for_flat_surface))
        ZCoordinatelist_3D.append(float(Point))

        for Steps_Neg in range(intsteps-1, 0, -1):
            # Set 3D NEG
            XCoordinate_Neg = Steps_Neg*0.5
            YCoordinate_Neg = Canoe_curve_function_inside.subs(
                x, XCoordinate_Neg)
            YCoordinate_Neg = round(YCoordinate_Neg, 4)
            XCoordinatelist_3D.append(float(XCoordinate_Neg*-1))
            YCoordinatelist_3D.append(
                float(YCoordinate_Neg+Height_for_flat_surface))
            ZCoordinatelist_3D.append(float(Point))

        # Connect back to zero
        XCoordinatelist_3D.append(float(0.0))
        YCoordinatelist_3D.append(float(0.0+Height_for_flat_surface))
        ZCoordinatelist_3D.append(float(Point))

        Dataframe_Coordniate = pd.DataFrame(Coordniatedict)

        print(Dataframe_Coordniate)
        print("\n")

        return(XCoordinatelist_3D, YCoordinatelist_3D, ZCoordinatelist_3D)


class Dataframewindow(Toplevel):

    def __init__(self, master=None):

        super().__init__(master=master)
        self.title("DataFrame")
        self.table = pt = Table(
            self, dataframe=Canoedesignprogram.Canoe_data_Spreadsheet,
            showtoolbar=True, showstatusbar=True)
        pt.show()


class Insturctionwindow(Toplevel):

    def __init__(self):
        super().__init__()

        self.title('Insturction information')
        self.option_add('*Font', 'Times')
        self.resizable(0, 0)
        """self.geometry("600x750")"""

        self.setinformation()

    def setinformation(self):

        self.scrollBar = Scrollbar(self)
        self.scrollBarX = Scrollbar(self, orient="horizontal")
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.scrollBarX.pack(side=BOTTOM, fill=X)

        self.listbox = tk.Listbox(
            self, width=90, yscrollcommand=self.scrollBar.set, xscrollcommand=self.scrollBarX.set)

        self.listbox.pack(side=LEFT, fill=BOTH)

        textbox = ["                                                              Introduction Page", "\n", "0. Understand Variables", "\n", "1. Canoe Length: Canoe length is the full length of the canoe, the length from its front to end, unit is Inch.", "2. Canoe Width: Canoe width is the full with of the canoe, the width from its left to right, unit is Inch.",
                   "3. Canoe Depth: Canoe depth is the full depth of the canoe, the depth from its bottom to top, unit is Inch.",
                   "4. Canoe Density: Canoe density is the density of the concrete, unit is lbs per cubic feet.",
                   "5. Canoe Thickness: Canoe density is the density of the concrete, unit is lbs per cubic feet.",
                   "6. Exponent of Curve functio: The exponent of the curve controls how flat the canoe is at the bottom."
                   + "\n"+" The larger the exponent, the flatter the bottom of the canoe is.",
                   "7. Exponent of Width function: The exponent of top view function curve controls how sharp the canoe is. It is less than or equal to 1."
                   + "\n"+" The larger the exponent, the sharper the front of the canoe is viewed from the front.",
                   "8. Exponent of Depth function: The exponent of the side view function controls how sharp the canoe is. It is less than or equal to 1."
                   + "\n"+" The larger the exponent, the sharper the front of the canoe is viewed from the side.",
                   "9. Thickness of Cover: Thickness of cover is the thickness of the concrete that cover the sterophom part from top, unit is inch.",
                   "10. Length of cover: Length of cover is the length of the sterophom part, or the part that is solid instead of empty, unit is inch.",
                   "11. Weight of crew: Weight of crew is the max weight of 4 crews, unit is lbs.", "\n",
                   "                                                               1. How to use the program", "\n", "1. You should input the canoe's data by typing them into the entry box."
                   + "\n"+"Data can be integer or decimal, positive or negetive, but must no be string.",
                   "2. After you input the data, press [Input Data] to save data. "+"\n"
                   + "Then, click [Cal data] to calculat data such as bouyancy, volume and etc "
                   + "\n"
                   + "To show your result, click [Show Dataframe] to display data as spreadsheet, you can download it as csv file.",
                   "3. Press [Find Best result] to find the lightest canoe that can pass submerge test and carry your 4 crew, its own weight and extra 150 lbs."]

        for item in textbox:
            self.listbox.insert(tk.END, item)

        self.scrollBar.config(command=self.listbox.yview)
        self.scrollBarX.config(command=self.listbox.xview)


if __name__ == "__main__":
    app = Canoedesignprogram()
    app.mainloop()
