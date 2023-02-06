&emsp;Canoe Design Program (CDP) is design software that aids the design process of the
canoe. The CDP will take mathematical inputs such as length, width, depth, the slope of the
curve, density, and crew weight to calculate the volume, buoyancy, center of gravity, and
waterline, determining the flow-ability of the canoe. Then, the CDP will generate an STL
(Standard Triangle Language) file that is water-tight, 3D printable, and testable in CFD
(Computational fluid dynamics) software.    

&emsp;Both calculating and model generating processes can be done manually by using a
calculator and CAD software. However, manual methods often confront tremendous efficiency
counter-backs considering the voluminous data, a large number of dimensions, and the
complexity of functions. For example, manual calculations tend to consume more time when
altering parameters and specifications to calculate and construct new models.

&emsp;CDP automates this process, heavily increasing efficiency, and ensuring accuracy.

**Important for vs code user**: YOU MUST FOLLOW THE \
INSTRUCTION ENTITLED "VScode tutorial Run.pdf" TO \
Run the Program.

You can see that there is a design example in the file,
use it as your canoe shape standard if you want.

It contains 7 mian code file, which are:\
1.MainGUI.py\
2.CanoeDataBase.py\
3.HealthCheck.py\
4.Calculation.py\
5.DataCalculation.py\
6.ModelCalculation.py\
7.OptimizationCalculation.py


Requirement:\
under the system root of SYDP-Project/code/source\
use command: pip install -r requirements.txt

Packages include:\
matplotlib\
numpy\
numpy_stl\
Pillow\
PyQt5\
scipy\
stl\
pathlib

#

Introduction:
* **important**:
MainGUi : (Graphic User Interface file) is the file\
that you should run, which will start the software
* To properly use this software, you must input proper data\
to access the functions of the software. Otherwise, the software
will not generate proper result.
* It is **highly** recommend to read the introduction document to 
understand the meaning of variables and the type of hulls \
that you can design.
* You can access the debug mode by clicking the button\
type in "help" to check how to use debug mode
