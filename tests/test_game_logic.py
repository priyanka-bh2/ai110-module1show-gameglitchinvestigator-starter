from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

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


def test_new_game_resets_app_state(monkeypatch):
    """Simulate pressing the New Game button and verify Streamlit session state is reset.

    This targets the bug where starting a new game did not reset `st.session_state.status`,
    preventing the UI from continuing after a win/loss.
    """
    import importlib
    import streamlit as st

    # Start from a finished game state
    st.session_state.clear()
    st.session_state.status = "won"
    st.session_state.attempts = 5
    st.session_state.score = 123
    st.session_state.history = [10, 20]

    # Make only the New Game button return True (simulate user click)
    def fake_button(label, *args, **kwargs):
        return label == "New Game 🔁"

    monkeypatch.setattr(st, "button", fake_button)

    # Provide safe defaults for other Streamlit inputs used during import
    monkeypatch.setattr(st.sidebar, "selectbox", lambda *a, **k: "Normal")
    monkeypatch.setattr(st, "text_input", lambda *a, **k: "")
    monkeypatch.setattr(st, "checkbox", lambda *a, **k: False)

    # Reload the app module so top-level UI logic runs with our patched button
    import app
    importlib.reload(app)

    # After New Game, state should be reset to a playable state
    assert st.session_state.status == "playing"
    assert st.session_state.score == 0
    assert st.session_state.history == []
    assert st.session_state.attempts == 0

    # Secret should be within the difficulty range (Normal -> 1..100)
    low, high = app.get_range_for_difficulty("Normal")
    assert low <= st.session_state.secret <= high


def test_changing_difficulty_resets_and_regenerates_secret(monkeypatch):
    """Changing the sidebar difficulty should reset the game and pick a new secret

    This reproduces the bug where changing difficulty updated the displayed range
    but did not regenerate the secret or reset attempts/score/history.
    """
    import importlib
    import streamlit as st

    # Start from a clean session and load app with Normal difficulty
    st.session_state.clear()
    monkeypatch.setattr(st.sidebar, "selectbox", lambda *a, **k: "Normal")
    # Provide safe defaults for other Streamlit inputs used during import
    monkeypatch.setattr(st, "text_input", lambda *a, **k: "")
    monkeypatch.setattr(st, "checkbox", lambda *a, **k: False)
    # Make buttons return False so import doesn't trigger New Game
    monkeypatch.setattr(st, "button", lambda *a, **k: False)

    import app
    importlib.reload(app)

    secret_normal = st.session_state.secret
    # Mutate session by making a guess to change attempts/score/history
    st.session_state.attempts = 3
    st.session_state.score = 50
    st.session_state.history = [10, 20]

    # Now reload the app with Hard selected; app should detect difficulty change
    monkeypatch.setattr(st.sidebar, "selectbox", lambda *a, **k: "Hard")
    importlib.reload(app)

    # Difficulty should be updated and game state reset
    assert st.session_state.current_difficulty == "Hard"
    assert st.session_state.attempts == 0
    assert st.session_state.score == 0
    assert st.session_state.history == []

    # Secret should be within the Hard difficulty range
    from logic_utils import get_range_for_difficulty
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 500
    assert low <= st.session_state.secret <= high
