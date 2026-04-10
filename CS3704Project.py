# CS 3704 Project
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import QTimer, QTime

class App_Functions(QWidget): # i dont like object orianted programmering but this works and im not gonna change that
    
    
    def __init__(self):
        super().__init__() # something important about accessing other functions i guess
        self.setWindowTitle("APP APP") # dont put exclimation marks
        self.layout = QVBoxLayout()
        self.label = QLabel("Im gonna update once per second", self)
        self.layout.addWidget(self.label) # add label to layout
        button = QPushButton("Press me") # make button to start app
        button.clicked.connect(self.on_click)
        self.layout.addWidget(button)
        self.setLayout(self.layout) # does something important
        self.started = False

        #this is the only timer you should use, import time makes the thing BREAK!!!
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.one_second_passed)
        self.seconds_past = 0 # variable definition. i tried it extenrally but it HATED that so define stuff here i guess?
       
    def on_click(self):
        self.started = True
        self.timer.start(1000) # in ms, so 1000 is one second

    def one_second_passed(self): # this is basicly a defined function
        self.seconds_past = self.seconds_past + 1 # incrementor
        self.label.setText(f"le epic u wasted {self.seconds_past} seconds looking at this")
       
app = QApplication(sys.argv) # makes the app appear
window = App_Functions()
window.show()
sys.exit(app.exec()) # dont delay running this. the window will still process on system exit but the thing will freeze if system exit is delayed.
