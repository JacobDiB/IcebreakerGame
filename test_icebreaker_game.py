import sys
import pytest
from PyQt6.QtWidgets import QApplication

from CS3704Project import App_Functions


# creates tetsing interface
@pytest.fixture
def app():
    test_app = QApplication.instance()

    if test_app is None:
        test_app = QApplication(sys.argv)

    return test_app


# makes fresh game
@pytest.fixture
def window(app):
    game = App_Functions()
    game.game_setup_menu()
    return game


def test_game_setup_stores_players_and_lives(window):
    #set up info
    window.players_input.setText("3")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Patrick, Danial")

    # start game
    window.start_game()

    # check setup info
    assert window.num_players == 3
    assert window.num_lives == 2
    assert window.player_names == ["Jacob", "Patrick", "Danial"]

    # check player lives
    assert window.lives == {
        "Jacob": 2,
        "Patrick": 2,
        "Danial": 2
    }


def test_invalid_setup_shows_error_message(window):
    # should be invalid
    window.players_input.setText("2")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Patrick")

    #  try tostart game
    window.start_game()

    # check error message
    assert window.label.text() == "Number of players must be greater than 2"


def test_submit_response_saves_answer(window):
    # set up the players for the round
    window.num_players = 3
    window.player_names = ["Jacob", "Patrick", "Danial"]

    # prompt round starts
    window.start_prompt_round()

    # Jacob submits answer
    window.response_input.setText("Interstellar")
    window.submit_response()

    # check that Jacob's answer was saved
    assert window.responses["Jacob"] == "Interstellar"

    # check that the game moved to the next player
    assert window.current_player_index == 1
    assert window.player_label.text() == "Patrick, enter your response:"


def test_vote_screen_creates_dropdowns(window):
    # give the game fake responses so it can build the voting screen
    window.player_names = ["Jacob", "Patrick", "Danial"]
    window.responses = {
        "Jacob": "Interstellar",
        "Patrick": "Cars",
        "Danial": "Shrek"
    }

    # open the vote screen
    window.vote()

    # there should be one dropdown for each response
    assert len(window.vote_boxes) == 3


def test_correct_guess_removes_one_life(window):
    # give the game players, lives, and responses
    window.player_names = ["Jacob", "Patrick", "Danial"]
    window.lives = {
        "Jacob": 2,
        "Patrick": 2,
        "Danial": 2
    }
    window.responses = {
        "Jacob": "Interstellar",
        "Patrick": "Cars",
        "Danial": "Shrek"
    }

    # pen the vote screen
    window.vote()

    # guess Jacob correctly, guess everyone else wrong
    window.vote_boxes["Jacob"].setCurrentText("Jacob")
    window.vote_boxes["Patrick"].setCurrentText("Jacob")
    window.vote_boxes["Danial"].setCurrentText("Jacob")

    # check the votes.
    window.check_votes()

    # only Jacob should lose a life.
    assert window.lives["Jacob"] == 1
    assert window.lives["Patrick"] == 2
    assert window.lives["Danial"] == 2

def test_duplicate_names_show_error_message(window):
    # This is invalid because two players have the same name.
    window.players_input.setText("3")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Jacob, Danial")

    # Try to start the game.
    window.start_game()

    # Check that the duplicate name error message appears.
    assert window.label.text() == "Player names must be unique"