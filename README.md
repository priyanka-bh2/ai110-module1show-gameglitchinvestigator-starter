# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

The game's purpose is to be a simple Streamlit number guessing game where the player tries to guess a hidden secret number within a limited number of attempts, using "higher" or "lower" hints to narrow it down. When I first ran it, the UI loaded fine but the game itself was unreliable: hints were often wrong, guesses outside the valid range behaved strangely, the New Game button didn’t fully reset the round, and difficulty settings didn’t actually change how the game played. I used GitHub Copilot Chat in VS Code to trace these issues to the `check_guess` logic (inverted hints and int/str comparisons), broken state handling around `st.session_state.status`, and incorrect difficulty ranges and secret generation. I fixed the logic by refactoring `check_guess` and `get_range_for_difficulty` into `logic_utils.py`, correcting the comparisons and ranges, and updating the New Game and difficulty-change handlers to reset session state properly and regenerate the secret using the selected difficulty. Finally, I added pytest tests around hint behavior, New Game resets, and difficulty changes, and verified the fixes by manually playing the game while watching the Developer Debug Info.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects **Normal** difficulty in the sidebar (range 1–100, attempts allowed: 7).
2. The app displays: “Guess a number between 1 and 100. Attempts left: 7”.
3. User enters a first guess of **20** and clicks **Submit Guess 🚀**.
4. The game responds with the hint **"📈 Go HIGHER!"** and updates the attempts left to 6.
5. User enters **70**; the game responds **"📉 Go LOWER!"**, and attempts left decreases to 5.
6. User enters **60** and sees **"🎉 Correct!"**, with the status in Developer Debug Info set to `"won"` and the score updated.
7. The user clicks **New Game 🔁**; attempts reset to 0, score and history clear, status becomes `"playing"`, and a new secret is chosen in the same difficulty range.
8. The user changes difficulty to **Hard**; the range label updates to **1–500**, the game state resets again, and a new secret is drawn within that larger range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```bash
# Full suite
python3 -m pytest -q
# 13 passed in 0.39s

# Single challenge test
python3 -m pytest tests/test_game_logic.py::test_changing_difficulty_resets_and_regenerates_secret -q
# 1 passed in 0.42s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
