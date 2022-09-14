import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from matplotlib.pyplot import MultipleLocator


app = QApplication(sys.argv)
screen = app.screens()[0]
mydpi = screen.physicalDotsPerInch()
app.quit()




fig = plt.figure(figsize=(1800/mydpi, 1800/mydpi), dpi=mydpi)
plt.plot([0,1,2,3],[1,1,2,2], ".")
x_major_locator=MultipleLocator(0.5)
y_major_locator=MultipleLocator(0.5)
ax=plt.gca()

ax.xaxis.set_major_locator(x_major_locator)
ax.yaxis.set_major_locator(y_major_locator)


plt.xlim(0,12.75)
plt.ylim(0,12.75)
plt.savefig("test_src1.pdf",format="pdf",dpi= mydpi)

