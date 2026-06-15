# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

_Fixes committed in `591947e`: corrected difficulty ranges, implemented reset-on-difficulty-change, and added tests (13 passing)._ 

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game, it showed a Streamlit page with a number guessing interface, a “Developer Debug Info” section, and buttons to submit a guess or start a new game, with attempts remaining shown at the top. The basic UI loaded correctly, but the game logic quickly felt unreliable once I started playing. Several hints were clearly wrong, guesses outside the 1–100 range behaved strangely, and the “New Game” button did not reliably reset the round. These issues made it hard to trust the feedback or even tell when a game had truly restarted.



- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

Bug 1 – Wrong hint at lower bound (guess of 1):
When I guessed 1 (the minimum allowed value), the game sometimes told me to “go lower,” which is impossible because the instructions say to guess between 1 and 100. I expected either “too low,” “too high,” or “correct,” but not a hint that points outside the valid range.

Bug 2 – Out-of-range guesses give nonsense hints:
When I entered a number far outside the 1–100 range (for example, 567), I expected the game to reject the input or remind me to stay within the allowed range. Instead, the game sometimes responded with “go higher,” which makes no sense for a guess that is way above any valid secret number.

Bug 3 – “New Game” does not fully restart:
Pressing the “New Game” button did not consistently reset the round. I expected it to pick a new secret number, reset attempts, and clear the previous hints, but instead the game often kept the old state so it felt like I was still in the previous game.

Bug 4 – Hints reversed or inconsistent:
Even when I could see the secret number in the Developer Debug Info (for example, secret = 60), the hints were sometimes reversed. If I guessed 13, I expected a hint like “go higher,” but the game told me to “go lower” instead, which is the opposite of the correct guidance.

Bug 5 – Difficulty settings have no effect:
The game shows a Settings panel where I can choose a difficulty level (for example, Easy with range 1–20 and 6 attempts), but changing the difficulty does not actually change how the game behaves. I expected the secret number range and allowed attempts to update when I select a different difficulty, but the game continued to behave as if it were using the default settings, ignoring the UI values



**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input / Action                                      | Expected Behavior                                                           | Actual Behavior                                                                                 | Console Output / Error |
|-----------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------|
| Secret in debug: 50; Guess: 1                      | Game says the guess is too low or at least does not tell me to go lower    | Game shows a hint telling me to “go lower,” which is impossible for the minimum value          | none                   |
| Secret in debug: 60; Guess: 13                     | Game says to go higher (13 is less than 60)                                | Game shows a “go lower” style hint, which is the opposite of what should happen                | none                   |
| Guess: 567 (range shown as 1–100)                  | Game rejects the input or reminds me to stay between 1 and 100             | Game sometimes responds with “go higher,” even though 567 is already above any valid number    | none                   |
| Finish a game, then click **New Game**             | Secret, attempts, score, and history all reset for a fresh round           | Some state carries over (status, attempts, or history), so it feels like I’m still in old game | none                   |
| Change difficulty from Easy to Hard in sidebar     | Range and secret update; game feels harder with a larger range and attempts reset | Range label changes, but the secret often stays from previous difficulty until I hit New Game | none                   |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I primarily used GitHub Copilot Chat inside VS Code, along with a separate chat-based AI assistant (like ChatGPT) to sanity-check logic and help phrase my reflection. Most of the in-editor debugging, refactoring, and test generation was done through Copilot’s local chat/agent in my VS Code workspace.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
For the wrong-hint bug (guessing 1 and seeing “go lower”), I used GitHub Copilot’s local chat agent in VS Code. I asked it to explain which code caused that behavior, and it identified the check_guess function as the root cause, pointing out that the hint messages were inverted and that the code was sometimes comparing integers to strings, falling back to lexicographic string comparison. The agent suggested fixing the swapped hint text, always comparing numeric values, and then refactoring check_guess into logic_utils.py as a reusable helper. I accepted this suggestion, let the agent move the function and add a separate get_hint_message helper, and then verified the behavior by running pytest (all tests passed) and replaying the game to confirm guesses like 1 and 13 now produced correct “go higher”/“go lower” hints.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
At one point the agent proposed leaving the alternating secret = str(...) conversion in place and relying on check_guess to coerce everything back to integers. This technically worked, but it felt unnecessarily complex and fragile, since it still mixed types and depended on hidden conversions. After reviewing the diff, I decided to simplify further by removing the string conversion in app.py so the secret stays an integer, which made the code easier to reason about. This was an example where the AI’s fix was “good enough,” but my own judgment pushed it toward a cleaner solution.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was really fixed only if I could reliably reproduce it before the change and then fail to reproduce it using the same inputs and steps afterward. For each bug, I kept a small text log of the exact guesses, difficulty, and expected vs actual behavior, and used that as a before/after checklist. I also required that both my automated tests and a manual playthrough of the game showed consistent, correct behavior (for example, hints matching the secret number and New Game fully resetting state) before I considered a fix done.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
One key test I ran was a pytest that directly called the check_guess function with a fixed secret number, such as 60, and several guesses like 1, 13, and values greater than 60. The test asserted that each guess returned the correct outcome string: “Too Low” for guesses below 60, “Too High” for guesses above 60, and “Win” for the exact match. When this test passed, it showed me that the core comparison logic and the high/low behavior were now correct and no longer inverted, which matched what I saw when I replayed the game in the browser.
- Did AI help you design or understand any tests? How?
AI helped me both design and understand my tests by suggesting concrete pytest examples based on the bugs I described. For instance, after I explained the New Game reset issue, the assistant proposed a test that simulates clicking the New Game button and then checks that st.session_state fields like status, attempts, score, history, and secret are reset correctly. It also suggested parameterized tests for check_guess, which made it easier to cover multiple input cases with less code. I still reviewed and edited those tests to match my actual logic, but the AI sped up the process of turning my bug descriptions into precise assertions.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I learned that Streamlit reruns the entire script from top to bottom every time the user interacts with the app, such as submitting a guess or pressing the New Game button. That means normal Python variables are recreated on each run, so anything you want to persist between interactions must be stored in st.session_state. In this game, things like the secret number, current attempts, score, and “status” all live in session state so they survive reruns. To a friend, I’d say Streamlit is constantly “refreshing” your code, and session_state is like a small backpack the app carries between refreshes so it doesn’t forget the current game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
One habit I want to reuse is writing down clear, reproducible bug cases before touching the code, including the exact inputs, expected behavior, and actual behavior. That simple “bug log” made it much easier to see whether my fixes actually worked and gave me concrete scenarios to turn into pytest tests. I also liked using focused prompts with my AI assistant that referenced specific files or functions instead of asking for broad refactors.
- What is one thing you would do differently next time you work with AI on a coding task?
Next time I work with AI on a coding task, I want to be more disciplined about limiting how many files it is allowed to modify at once. In a few cases, the agent tried to fix the problem by changing multiple functions and adding helper files, which made it harder to understand what truly fixed the bug. I’d rather ask for smaller, incremental changes, review each diff carefully, and run tests after every meaningful change.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project made me see AI-generated code less as “magic that just works” and more as a fast but fallible collaborator. I now think of AI as a useful assistant for ideas, boilerplate, and tests, but I rely on my own debugging, understanding of state, and test results to decide what to accept, modify, or reject.
