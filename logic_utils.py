def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # Normalize to integers when possible to avoid lexicographic compares
    try:
        g = int(guess)
    except Exception:
        return "Invalid", "That is not a number."

    try:
        s = int(secret)
    except Exception:
        # Secret should always be numeric; if not, treat as internal error
        return "Invalid", "Internal error: secret not numeric."

    if g == s:
        return "Win"

    if g > s:
        return "Too High"

    return "Too Low"


def get_hint_message(outcome: str):
    """Return a user-friendly hint message for an outcome string."""
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
