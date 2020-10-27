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

def number_to_emoji(n: int) -> str:
    return NUMBER_TO_EMOJI[n]

def emoji_to_number(e: str) -> int:
    return EMOJI_TO_NUMBER[e]
