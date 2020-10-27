from typing import Optional

NUMBER_TO_EMOJI = {
    0: "0⃣",
    1: "1⃣",
    2: "2⃣",
    3: "3⃣",
    4: "4⃣",
    5: "5⃣",
    6: "6⃣",
    7: "7⃣",
    8: "8⃣",
    9: "9⃣",
}

EMOJI_TO_NUMBER = {v: k for k, v in NUMBER_TO_EMOJI.items()}

def number_to_emoji(n: int) -> Optional[str]:
    return NUMBER_TO_EMOJI.get(n, None)

def emoji_to_number(e: str) -> Optional[int]:
    return EMOJI_TO_NUMBER.get(e, None)
