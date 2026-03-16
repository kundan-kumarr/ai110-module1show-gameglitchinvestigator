import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

if __name__ == "__main__":
    tests = [test_winning_guess, test_guess_too_high, test_guess_too_low]
    for t in tests:
        try:
            t()
            print(f"PASSED: {t.__name__}")
        except AssertionError as e:
            print(f"FAILED: {t.__name__} — {e}")
