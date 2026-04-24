import sys
import pytest
from PyQt6.QtWidgets import QApplication

from CS3704Project import App_Functions


@pytest.fixture
def app():
    test_app = QApplication.instance()

    if test_app is None:
        test_app = QApplication(sys.argv)

    return test_app


@pytest.fixture
def window(app):
    game = App_Functions()
    game.game_setup_menu()
    return game


def test_start_game_creates_player_lives(window):
    window.players_input.setText("3")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Patrick, Danial")

    window.start_game()

    assert window.num_players == 3
    assert window.num_lives == 2
    assert window.player_names == ["Jacob", "Patrick", "Danial"]
    assert window.lives["Jacob"] == 2
    assert window.lives["Patrick"] == 2
    assert window.lives["Danial"] == 2


def test_start_game_rejects_invalid_numbers(window):
    window.players_input.setText("three")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Patrick, Danial")

    window.start_game()

    assert window.label.text() == "Enter valid numbers"


def test_start_game_rejects_invalid_player_count(window):
    window.players_input.setText("2")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Patrick")

    window.start_game()

    assert window.label.text() == "Number of players must be greater than 2"


def test_start_game_rejects_invalid_life_count(window):
    window.players_input.setText("3")
    window.lives_input.setText("0")
    window.names_input.setText("Jacob, Patrick, Danial")

    window.start_game()

    assert window.label.text() == "Lives must be greater than 0"


def test_start_game_rejects_name_count_mismatch(window):
    window.players_input.setText("3")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, Patrick")

    window.start_game()

    assert window.label.text() == "Names must match number of players"


def test_start_prompt_round_sets_first_player(window):
    window.num_players = 3
    window.num_lives = 2
    window.player_names = ["Jacob", "Patrick", "Danial"]

    window.start_prompt_round()

    assert window.current_player_index == 0
    assert window.responses == {}
    assert window.prompt == "What is your favorite movie?"
    assert window.player_label.text() == "Jacob, enter your response:"


def test_submit_response_saves_answer_and_moves_to_next_player(window):
    window.num_players = 3
    window.num_lives = 2
    window.player_names = ["Jacob", "Patrick", "Danial"]
    window.start_prompt_round()

    window.response_input.setText("Interstellar")
    window.submit_response()

    assert window.responses["Jacob"] == "Interstellar"
    assert window.current_player_index == 1
    assert window.player_label.text() == "Patrick, enter your response:"


def test_submit_response_rejects_empty_answer(window):
    window.num_players = 3
    window.num_lives = 2
    window.player_names = ["Jacob", "Patrick", "Danial"]
    window.start_prompt_round()

    window.response_input.setText("")
    window.submit_response()

    assert window.player_label.text() == "Response cannot be empty"
    assert window.current_player_index == 0


def test_vote_creates_dropdowns_for_each_response(window):
    window.player_names = ["Jacob", "Patrick", "Danial"]
    window.responses = {
        "Jacob": "Interstellar",
        "Patrick": "Cars",
        "Danial": "Shrek"
    }

    window.vote()

    assert len(window.vote_boxes) == 3
    assert "Jacob" in window.vote_boxes
    assert "Patrick" in window.vote_boxes
    assert "Danial" in window.vote_boxes


def test_check_votes_removes_life_for_correct_guess(window):
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

    window.vote()

    window.vote_boxes["Jacob"].setCurrentText("Jacob")
    window.vote_boxes["Patrick"].setCurrentText("Jacob")
    window.vote_boxes["Danial"].setCurrentText("Jacob")

    window.check_votes()

    assert window.lives["Jacob"] == 1
    assert window.lives["Patrick"] == 2
    assert window.lives["Danial"] == 2


def test_full_one_prompt_integration(window):
    window.players_input.setText("3")
    window.lives_input.setText("1")
    window.names_input.setText("Jacob, Patrick, Danial")

    window.start_game()

    window.response_input.setText("Interstellar")
    window.submit_response()

    window.response_input.setText("Cars")
    window.submit_response()

    window.response_input.setText("Shrek")
    window.submit_response()

    assert len(window.vote_boxes) == 3

    window.vote_boxes["Jacob"].setCurrentText("Jacob")
    window.vote_boxes["Patrick"].setCurrentText("Patrick")
    window.vote_boxes["Danial"].setCurrentText("Danial")

    window.check_votes()

    assert window.lives["Jacob"] == 0
    assert window.lives["Patrick"] == 0
    assert window.lives["Danial"] == 0

def test_blank_player_name_shows_error_message(window):
    # This setup is invalid because one player name is blank.
    window.players_input.setText("3")
    window.lives_input.setText("2")
    window.names_input.setText("Jacob, , Danial")

    # Try to start the game.
    window.start_game()

    # The game should show an error message and not continue.
    assert window.label.text() == "Player names cannot be blank"