def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive guess range.
        Defaults to (1, 100) for unrecognised difficulty values.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Accepts whole numbers and decimals (decimals are truncated, not rounded).
    Returns a 3-tuple so callers can branch on success without catching exceptions.

    Args:
        raw: The raw string typed by the user, or None if the field is empty.

    Returns:
        A tuple ``(ok, guess_int, error_message)`` where:
        - ``ok`` is True if parsing succeeded, False otherwise.
        - ``guess_int`` is the parsed integer on success, None on failure.
        - ``error_message`` is a human-readable string on failure, None on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.9")
        (True, 3, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a player's guess to the secret number and return feedback.

    Args:
        guess: The player's guessed integer.
        secret: The secret integer the player is trying to match.

    Returns:
        A tuple ``(outcome, message)`` where:
        - ``outcome`` is one of ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        - ``message`` is a short, emoji-decorated hint string for the player.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(40, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate a new score based on the outcome of the latest guess.

    Scoring rules:
    - **Win**: awards ``max(10, 100 - 10 * (attempt_number + 1))`` points.
    - **Too High** on an even attempt: +5 points (lucky bonus).
    - **Too High** on an odd attempt: -5 points.
    - **Too Low**: -5 points always.

    Args:
        current_score: The player's score before this guess.
        outcome: One of ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        attempt_number: The 1-based attempt count for the current guess.

    Returns:
        The updated integer score after applying the outcome's point change.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(50, "Too Low", 3)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
