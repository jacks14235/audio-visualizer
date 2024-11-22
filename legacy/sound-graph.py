import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer
import time


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.looping = False
        self.width = 800
        self.height = 800
        self.timer = QTimer()
        self.yellow = False
        self.timer.timeout.connect(self.setColors)
        self.initUI()
        print("Done")
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()

        buttons = []
        
        boxes_per_side = 12
        start = QPushButton('Start')
        start.clicked.connect(self.changeLoop)
        layout.addWidget(start, 0, boxes_per_side // 2)
        for i in range(boxes_per_side):
            for j in range(boxes_per_side):
                button = QPushButton('')
                buttons.append(button)
                layout.addWidget(button,i+1,j)
        
        self.horizontalGroupBox.setLayout(layout)
        self.buttons =  buttons
    
    def changeLoop(self):
        self.timer.start(1000)

    
    def setColors(self):
        print("Here")

        if not self.yellow:
            for button in self.buttons: 
                button.setStyleSheet(f'background-color : yellow')
            self.yellow = True
        else:
            for button in self.buttons: 
                button.setStyleSheet(f'background-color : blue')
            self.yellow = False
        self.timer.start(1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("1")
    ex = App()
    # for i in range(144):
    #     ex.setColors(i)
    #     time.sleep(1)
    sys.exit(app.exec_())
    print("3")