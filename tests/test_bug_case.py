from logic_utils import check_guess, get_hint_message


def test_guess_one_numeric_secret_shows_go_higher():
    # If secret is 2 and guess is 1, outcome should be Too Low
    outcome = check_guess(1, 2)
    assert outcome == "Too Low"
    assert get_hint_message(outcome) == "📈 Go HIGHER!"


def test_guess_one_string_secret_shows_go_higher():
    # If secret is "2" (string) and guess is 1, behavior should be the same
    outcome = check_guess(1, "2")
    assert outcome == "Too Low"
    assert get_hint_message(outcome) == "📈 Go HIGHER!"


def test_lexicographic_edge_case_prevented():
    # Lexicographic ordering would make "9" > "10"; ensure numeric compare used
    outcome = check_guess(9, "10")
    assert outcome == "Too Low"
    assert get_hint_message(outcome) == "📈 Go HIGHER!"


def test_guess_one_win_message():
    outcome = check_guess(1, 1)
    assert outcome == "Win"
    assert get_hint_message(outcome) == "🎉 Correct!"
