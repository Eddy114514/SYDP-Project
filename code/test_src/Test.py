from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
screen = app.screens()[0]
DPI_OF_DEVICE = screen.physicalDotsPerInch()
app.quit()

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.axis('off')
from matplotlib.pyplot import MultipleLocator


