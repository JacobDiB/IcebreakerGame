# CS 3704 Project
import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QFont
import random

default_font = QFont("Arial")
default_font.setPointSize(16)

prompt_font = QFont("Arial")
prompt_font.setPointSize(18)
prompt_font.setBold(True)

title_font = QFont("Arial")
title_font.setPointSize(26)
title_font.setBold(True)

main_button_font = QFont("Arial")
main_button_font.setPointSize(20)
main_button_font.setBold(True)

class App_Functions(QWidget): # i dont like object orianted programmering but this works and im not gonna change that
    
    
    def __init__(self):
        super().__init__() # something important about accessing other functions i guess
        
        self.num_players = 0
        self.num_lives = 0
        self.player_names = []

        # Game title
        self.setWindowTitle("Ice Breaker Game")
        self.layout = QVBoxLayout()

        self.main_menu()

    #def on_click(self):
    #    self.started = True
    #    self.timer.start(1000) # in ms, so 1000 is one second

    #def one_second_passed(self): # this is basicly a defined function
    #    self.seconds_past = self.seconds_past + 1 # incrementor
    #    self.label.setText(f"le epic u wasted {self.seconds_past} seconds looking at this")

    def clear_old(self):
        # clear old layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def main_menu(self):
        self.clear_old()
        
        self.label = QLabel("Ice Breaker Game")        
        self.label.setFont(title_font)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.layout.addWidget(self.label)


        self.button = QPushButton("Play!")
        self.button.clicked.connect(self.game_setup_menu)
        self.button.setFont(main_button_font)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def game_setup_menu(self):
        self.clear_old()
        
        self.label = QLabel("Enter game setup information")
        self.layout.addWidget(self.label)

        # Number of players entry box
        self.players_input = QLineEdit(self)
        self.players_input.setFont(default_font)
        self.players_input.setPlaceholderText("Enter number of players")
        self.layout.addWidget(self.players_input)

        # Number of lives entry box
        self.lives_input = QLineEdit(self)
        self.lives_input.setFont(default_font)
        self.lives_input.setPlaceholderText("Enter number of lives")
        self.layout.addWidget(self.lives_input)

        # Names entry box
        self.names_input = QLineEdit(self)
        self.names_input.setFont(default_font)
        self.names_input.setPlaceholderText("Enter player names (comma separated)")
        self.layout.addWidget(self.names_input)

        # Start game button
        self.button = QPushButton("Start Game")
        self.button.setFont(default_font)
        self.button.clicked.connect(self.start_game)
        self.layout.addWidget(self.button)

        # Timer
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.one_second_passed)
        #self.seconds_past = 0
        #self.started = False

        self.setLayout(self.layout)

       
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
        

        
        # check for duplicate player names
        if len(set(self.player_names)) != len(self.player_names):
            self.label.setText("Player names must be unique")
            return

        self.lives = {}
        # give each plyaer the starting number of lives
        for name in self.player_names:
            self.lives[name] = self.num_lives
        # success
        self.start_prompt_round()

    def start_prompt_round(self):
        self.clear_old()

        # initialize game state
        self.current_player_index = 0
        self.responses = {}

        # prompt
        self.prompt = "What is your favorite movie?"

        # prompt label
        self.prompt_label = QLabel(self.prompt)
        self.prompt_label.setFont(prompt_font)
        self.layout.addWidget(self.prompt_label)

        # player label
        self.player_label = QLabel("")
        self.player_label.setFont(default_font)
        self.layout.addWidget(self.player_label)

        # response input
        self.response_input = QLineEdit(self)
        self.response_input.setFont(default_font)
        self.layout.addWidget(self.response_input)

        # submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFont(default_font)
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
        # clear old responce screen
        self.clear_old()
        # discionary that connects player to votes
        self.vote_boxes = {}

        # title for voting screen
        title = QLabel("Guess who wrote each answer")
        title.setFont(prompt_font)
        self.layout.addWidget(title)

        #shuffle the answers
        response_items = list(self.responses.items())
        random.shuffle(response_items)

        # make label and dropdown per player
        for real_player, response in response_items:
            response_label = QLabel(f"Answer: {response}")
            response_label.setFont(default_font)
            self.layout.addWidget(response_label)

            box = QComboBox()
            box.setFont(default_font)
            box.addItems(self.player_names)
            self.layout.addWidget(box)

            self.vote_boxes[real_player] = box

        # button for submitting all guesses
        submit_votes_button = QPushButton("Submit Votes")
        submit_votes_button.setFont(default_font)
        submit_votes_button.clicked.connect(self.check_votes)
        self.layout.addWidget(submit_votes_button)

    def check_votes(self):
        # clear voting screen
        self.clear_old()

        result_title = QLabel("Round Results")
        result_title.setFont(prompt_font)
        self.layout.addWidget(result_title)

        # cheack the guesses to the real answers
        for real_player in self.vote_boxes:
            # get the player name
            guessed_player = self.vote_boxes[real_player].currentText()

            # if guess matches player loses life
            if guessed_player == real_player:
                self.lives[real_player] -= 1
                result = QLabel(f"{real_player}'s answer was guessed correctly. They lose 1 life.")
            else:
                result = QLabel(f"{real_player}'s answer was not guessed correctly.")

            # show the result
            result.setFont(default_font)
            self.layout.addWidget(result)

        lives_title = QLabel("Lives Remaining")
        lives_title.setFont(prompt_font)
        self.layout.addWidget(lives_title)

        # show each players current life count
        for player in self.player_names:
            lives_label = QLabel(f"{player}: {self.lives[player]} lives")
            lives_label.setFont(default_font)
            self.layout.addWidget(lives_label)

        # check if any player lost all lives
        loser_found = False

        # check if any player has 0 lives
        for player in self.player_names:
            if self.lives[player] <= 0:
                loser_found = True
                loser_label = QLabel(f"Game over. {player} lost all of their lives.")
                loser_label.setFont(prompt_font)
                self.layout.addWidget(loser_label)

        # if someone lost return to main menu
        if loser_found:
            restart_button = QPushButton("Return to Main Menu")
            restart_button.setFont(default_font)
            restart_button.clicked.connect(self.main_menu)
            self.layout.addWidget(restart_button)
        # if nobody lost go back
        else:
            end_button = QPushButton("End Demo")
            end_button.setFont(default_font)
            end_button.clicked.connect(self.end_demo)
            self.layout.addWidget(end_button)

    def end_demo(self):
        # clear the screen
        self.clear_old()

        # show that round is finished
        end_label = QLabel("One full prompt round is complete.")
        end_label.setFont(prompt_font)
        self.layout.addWidget(end_label)

        # buttom to return to main menu
        menu_button = QPushButton("Return to Main Menu")
        menu_button.setFont(default_font)
        menu_button.clicked.connect(self.main_menu)
        self.layout.addWidget(menu_button)

if __name__ == "__main__": # make tetsing possible
    app = QApplication(sys.argv) # makes the app appear
    window = App_Functions()
    window.show()
    sys.exit(app.exec())# dont delay running this. the window will still process on system exit but the thing will freeze if system exit is delayed.
