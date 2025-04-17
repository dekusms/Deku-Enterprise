"""Password Validation Tests Module."""

import math
from collections import Counter
from pwnedpasswords import check as check_pwned


def test_length(password: str, min_length: int) -> tuple[bool, str]:
    """Check if the password meets the minimum length requirement."""
    if len(password) < min_length:
        return (
            True,
            f"The password must be at least {min_length} characters long.",
        )
    return False, ""


def test_uppercase(password: str, min_uppercase: int) -> tuple[bool, str]:
    """Check if the password contains the required number of uppercase letters."""
    if sum(1 for c in password if c.isupper()) < min_uppercase:
        return (
            True,
            f"Password must include at least {min_uppercase} uppercase letter(s).",
        )
    return False, ""


def test_numbers(password: str, min_numbers: int) -> tuple[bool, str]:
    """Check if the password contains the required number of numbers."""
    if sum(1 for c in password if c.isdigit()) < min_numbers:
        return True, f"Password must include at least {min_numbers} number(s)."
    return False, ""


def test_special_characters(
    password: str, min_special: int, allowed_specials: str
) -> tuple[bool, str]:
    """Check if the password contains the required number of special characters."""
    if sum(1 for c in password if c in allowed_specials) < min_special:
        return (
            True,
            f"Password must include at least {min_special} special character(s) "
            f"from the set: {allowed_specials}",
        )
    return False, ""


def test_pwned(password: str) -> tuple[bool, str]:
    """Check if the password has been found in data breaches."""
    try:
        pwned_count = check_pwned(password, plain_text=True)
        if pwned_count > 0:
            return (
                True,
                f"The password you entered has appeared in {pwned_count} data breaches. "
                "Please choose a more secure password to protect your account.",
            )
    except Exception:
        return (
            True,
            "Unable to verify if the password has been pwned. Please try again later.",
        )
    return False, ""


def test_entropy(password: str, min_entropy: float) -> tuple[bool, str]:
    """Check if the password's entropy meets the minimum requirement."""
    if not password:
        return True, "Password cannot be empty."

    # Calculate entropy
    length = len(password)
    frequency = Counter(password)
    entropy = -sum(
        (count / length) * math.log2(count / length) for count in frequency.values()
    )

    if entropy < min_entropy:
        return (
            True,
            f"The password is too weak. Entropy: {entropy:.2f} bits (min: {min_entropy} bits).",
        )
    return False, ""


def run_password_validation_tests(password: str, policy: dict) -> list:
    """
    Run the required password validation tests based on the policy.

    Args:
        password (str): The password to validate.
        policy (dict): The password policy.

    Returns:
        list: A list of test functions to run.
    """
    test_mapping = []

    if "min_length" in policy:
        test_mapping.append(lambda: test_length(password, policy["min_length"]))
    if "min_uppercase" in policy:
        test_mapping.append(lambda: test_uppercase(password, policy["min_uppercase"]))
    if "min_numbers" in policy:
        test_mapping.append(lambda: test_numbers(password, policy["min_numbers"]))
    if "min_special" in policy and "allowed_specials" in policy:
        test_mapping.append(
            lambda: test_special_characters(
                password, policy["min_special"], policy["allowed_specials"]
            )
        )
    if "check_pwned" in policy and policy["check_pwned"]:
        test_mapping.append(lambda: test_pwned(password))
    if "min_entropy" in policy:
        test_mapping.append(lambda: test_entropy(password, policy["min_entropy"]))

    return test_mapping
