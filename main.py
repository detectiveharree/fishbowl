import os
import logging
import sys


sys.setrecursionlimit(100000)
logging.basicConfig(level=logging.INFO)



message = """Random python hash seed: %s
Note. It is not possible to get completely deterministic launches each time run this program,
however you help by adding PYTHONHASHSEED=0 to the environment variable before running this program.
If "Random python hash seed" is False, it's worked.""" % (os.environ.get("PYTHONHASHSEED") != "0")

print(message)

import random
import numpy as np

"""
SET SEEDS FOR ENTIRE PROGRAM
"""
random.seed(10)
np.random.seed(10)

from PyQt5.QtWidgets import QApplication
import sys
import guiwindow


def main():


    app = QApplication(sys.argv)
    win = guiwindow.GUIWindow()
    win.show()
    sys.exit(app.exec_())


"""
This is just so we can see errors that happen on GUI threadp
"""
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__=="__main__":

    sys.excepthook = except_hook
    main()
