# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, the hints were completely backwards - guessing a number lower than the secret showed "Go LOWER!" and guessing higher showed "Go HIGHER!", which made the game unwinnable by logic. There was also a subtle type-conversion bug where on every even-numbered attempt the secret was silently cast to a string, so comparisons between the integer guess and the string secret fell into an error-handling path and produced wrong hints. A third issue was that the "New Game" button appeared to do nothing after a win or loss — clicking it showed the "New game started" message but the game was still stuck. The root cause was that the handler reset `attempts` and `secret` but never reset `st.session_state.status` back to `"playing"`, so the `st.stop()` block fired immediately on the next rerun and blocked the game. A fourth issue was that all the logic functions (`check_guess`, `parse_guess`, etc.) lived directly in `app.py` rather than in `logic_utils.py`, and the stubs in `logic_utils.py` all raised `NotImplementedError`.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic) as my primary AI assistant throughout this project. One correct suggestion was fixing the swapped hint messages in `check_guess` - the AI correctly identified that `guess > secret` should map to "Go LOWER!" not "Go HIGHER!", and I verified this by playing the game manually and confirming the hints matched my guesses. An example where AI output needed correction was the test file: the original AI-generated tests compared the full `(outcome, message)` tuple directly to a plain string like `"Win"`, which always failed — I had to understand the return type of `check_guess` myself and update the tests to unpack the tuple before asserting.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when the relevant pytest test passed AND I could manually confirm the behavior in the running Streamlit app. I ran `python -m pytest tests/ -v` from the project root, which collected three tests and showed all three failing before my fixes and all three passing after. The tests revealed that `check_guess` returns a tuple, not a plain string — something easy to miss just by reading the code but immediately obvious when pytest printed the `AssertionError: assert ('Win', '🎉 Correct!') == 'Win'` message. AI helped me understand that `conftest.py` is pytest-specific and won't be loaded when running a file with plain `python`, which led to adding a `__main__` block instead.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every single time the user interacts with the page - clicks a button, types in a box, changes a dropdown. If you store a variable normally (e.g., `secret = random.randint(1, 100)`), it gets a brand-new value on every rerun, which would make a guessing game impossible. `st.session_state` is a dictionary that persists across reruns, so wrapping initialization in `if "secret" not in st.session_state` means the secret is only generated once per game session, no matter how many times the script reruns. Think of it like a sticky note attached to the browser tab — regular variables are on a whiteboard that gets erased, while session state is on the sticky note.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is running the test suite immediately after every change, even small ones - it caught the tuple vs. string mismatch right away instead of letting it hide. Next time I work with AI on a coding task, I would read AI-generated test assertions more carefully before trusting them, since the AI confidently wrote tests that looked correct but were comparing incompatible types. This project changed how I think about AI-generated code: it can produce plausible-looking code that compiles and runs but contains subtle logic errors, so treating AI output as a first draft to verify rather than a finished answer is the right mindset.

---

## 6. AI Model Comparison (Challenge 5)

**Bug tested:** The swapped Higher/Lower hints in `check_guess` — `guess > secret` returning "Go HIGHER!" instead of "Go LOWER!".

**Claude Code (Anthropic)** identified the bug immediately by reading the conditional logic and explaining that if the guess is already above the secret the player needs to guess *lower*, not higher. It pointed directly to lines 37–40, showed the corrected version, and explained *why* the messages were wrong in one sentence before making the edit.

**ChatGPT (GPT-4o)** also found the correct fix but framed its response around a general explanation of how number-guessing hint logic works before getting to the specific lines. The fix itself was identical, but it took more reading to extract the actual change — it added a paragraph about "common AI coding mistakes" that wasn't directly useful.

**Verdict:** Both models produced the correct fix. Claude Code was more readable because it led with the change rather than the explanation, and it cited the exact line numbers. ChatGPT's explanation of *why* the bug is a common AI mistake was more thorough, which is useful if you're trying to understand the pattern rather than just fix this one instance.
