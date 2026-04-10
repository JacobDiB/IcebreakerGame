# CS 3704 Project
import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import QTimer, QTime

class App_Functions(QWidget): # i dont like object orianted programmering but this works and im not gonna change that
    
    
    def __init__(self):
        super().__init__() # something important about accessing other functions i guess
        
        self.num_players = 0
        self.num_lives = 0
        self.player_names = []

        # Game title
        self.setWindowTitle("Ice Breaker Game")
        self.layout = QVBoxLayout()
        self.label = QLabel("Enter game setup information")
        self.layout.addWidget(self.label)
        
        # Number of players entry box
        self.players_input = QLineEdit(self)
        self.players_input.setPlaceholderText("Enter number of players")
        self.layout.addWidget(self.players_input)

        # Number of lives entry box
        self.lives_input = QLineEdit(self)
        self.lives_input.setPlaceholderText("Enter number of lives")
        self.layout.addWidget(self.lives_input)

        # Names entry box
        self.names_input = QLineEdit(self)
        self.names_input.setPlaceholderText("Enter player names (comma separated)")
        self.layout.addWidget(self.names_input)

        # Start game button
        self.button = QPushButton("Start Game")
        self.button.clicked.connect(self.start_game)
        self.layout.addWidget(self.button)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.one_second_passed)
        self.seconds_past = 0
        self.started = False

        self.setLayout(self.layout)

    def on_click(self):
        self.started = True
        self.timer.start(1000) # in ms, so 1000 is one second

    def one_second_passed(self): # this is basicly a defined function
        self.seconds_past = self.seconds_past + 1 # incrementor
        self.label.setText(f"le epic u wasted {self.seconds_past} seconds looking at this")
       
    def start_game(self):
        players_text = self.players_input.text()
        lives_text = self.lives_input.text()
        names_text = self.names_input.text()

        # check if numbers are valid
        if not players_text.isdigit() or not lives_text.isdigit():
            self.label.setText("Enter valid numbers")
            return

        self.num_players = int(players_text)
        self.num_lives = int(lives_text)

        # split names
        self.player_names = names_text.split(",")

        # remove extra spaces
        for i in range(len(self.player_names)):
            self.player_names[i] = self.player_names[i].strip()

        # check values
        if self.num_players <= 0 or self.num_lives <= 0:
            self.label.setText("Players and lives must be > 0")
            return

        if len(self.player_names) != self.num_players:
            self.label.setText("Names must match number of players")
            return

        # success
        self.label.setText("Game started")
        self.started = True
        self.seconds_past = 0
        self.timer.start(1000)

app = QApplication(sys.argv) # makes the app appear
window = App_Functions()
window.show()
sys.exit(app.exec()) # dont delay running this. the window will still process on system exit but the thing will freeze if system exit is delayed.
