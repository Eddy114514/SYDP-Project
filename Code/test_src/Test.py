from pathlib import Path
a = Path("..//..//Code//source//Calculation.py")
AbsFilePath = __file__
AbsFilePath = AbsFilePath[0:AbsFilePath.index("Code")]
print(AbsFilePath)