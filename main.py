from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QFile, QTextStream, Qt
from sys import argv

import queries

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() 
        uic.loadUi('main.ui', self)
        self.show()
    
 
def main():
    app = QtWidgets.QApplication(argv)
    window = Ui()
    app.exec_()
    

main()