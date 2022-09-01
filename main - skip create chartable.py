#from tool import dbtool
import os
import sys
# from tool import dbtool
from gui import MainWindow
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # print("creating usertable object")
    # usertable = dbtool.UserTable()

    # print("creating chartable object")
    # chartable = dbtool.CharTable()

    # usertable.get_connected()
    # chartable.get_connected()

    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.Dialog)
    widget.show()

    sys.exit(app.exec_())
