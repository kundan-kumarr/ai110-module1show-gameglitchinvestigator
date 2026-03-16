import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess

# ── Core tests ────────────────────────────────────────────────────────────────

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

# ── Edge-case tests (Challenge 1) ─────────────────────────────────────────────

def test_negative_number():
    # Negative numbers should parse successfully and compare correctly
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_decimal_input():
    # Decimals should be truncated to int (e.g. 3.9 → 3)
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3

def test_very_large_number():
    # Extremely large values should parse and still return a valid outcome
    ok, value, err = parse_guess("999999999")
    assert ok is True
    outcome, message = check_guess(value, 50)
    assert outcome == "Too High"

def test_empty_string():
    # Empty input should fail gracefully with an error message
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_none_input():
    # None input should fail gracefully
    ok, value, err = parse_guess(None)
    assert ok is False
    assert err == "Enter a guess."

def test_non_numeric_string():
    # Letters should fail with a clear error message
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."

def test_whitespace_only():
    # Whitespace-only input should fail gracefully
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert err == "That is not a number."

if __name__ == "__main__":
    tests = [
        test_winning_guess, test_guess_too_high, test_guess_too_low,
        test_negative_number, test_decimal_input, test_very_large_number,
        test_empty_string, test_none_input, test_non_numeric_string,
        test_whitespace_only,
    ]
    for t in tests:
        try:
            t()
            print(f"PASSED: {t.__name__}")
        except AssertionError as e:
            print(f"FAILED: {t.__name__} — {e}")
