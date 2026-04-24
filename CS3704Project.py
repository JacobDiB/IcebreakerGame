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
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.one_second_passed)
        #self.seconds_past = 0
        #self.started = False

        self.setLayout(self.layout)

    #def on_click(self):
    #    self.started = True
    #    self.timer.start(1000) # in ms, so 1000 is one second

    #def one_second_passed(self): # this is basicly a defined function
    #    self.seconds_past = self.seconds_past + 1 # incrementor
    #    self.label.setText(f"le epic u wasted {self.seconds_past} seconds looking at this")
       
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
        if self.num_lives <= 0:
            self.label.setText("Lives must be greater than 0")
            return

        if self.num_players < 3:
            self.label.setText("Number of players must be greater than 2")
            return

        if len(self.player_names) != self.num_players:
            self.label.setText("Names must match number of players")
            return

        # success
        self.start_prompt_round()

    def start_prompt_round(self):
        # clear old layout
        for i in reversed(range(self.layout.count())): #should ensure that the program doesn't crash if a file is already empty, just in case
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.layout.removeItem(item)

        # initialize game state
        self.current_player_index = 0
        self.responses = {}

        # prompt
        self.prompt = "What is your favorite movie?"

        # prompt label
        self.prompt_label = QLabel(self.prompt)
        self.layout.addWidget(self.prompt_label)

        # player label
        self.player_label = QLabel("")
        self.layout.addWidget(self.player_label)

        # response input
        self.response_input = QLineEdit(self)
        self.layout.addWidget(self.response_input)

        # submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_response)
        self.layout.addWidget(self.submit_button)

        # show first player
        self.update_player_prompt()

    def update_player_prompt(self):
        current_player = self.player_names[self.current_player_index]
        self.player_label.setText(f"{current_player}, enter your response:")
        self.response_input.clear()

    def submit_response(self):
        response = self.response_input.text().strip()

        # if there's no response
        if not response:
            self.player_label.setText("Response cannot be empty")
            return

        current_player = self.player_names[self.current_player_index]
        self.responses[current_player] = response

        # go to next player
        self.current_player_index += 1

        # check if done
        if self.current_player_index >= self.num_players:
            self.vote()
        else:
            self.update_player_prompt()

    def vote(self):
        return


app = QApplication(sys.argv) # makes the app appear
window = App_Functions()
window.show()
sys.exit(app.exec()) # dont delay running this. the window will still process on system exit but the thing will freeze if system exit is delayed.
