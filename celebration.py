"""
celebrate.py

Deterministic celebration messages for coding exercises.

The celebration changes only when your Python code changes.
Comments and formatting are ignored by hashing each file's AST.
"""

from __future__ import annotations

import ast
import hashlib
import random
from pathlib import Path


# ---------------------------------------------------------------------------
# Loot tables
# ---------------------------------------------------------------------------

EMOJIS = {
    "common": [
        "🎉", "🎊", "✨", "⭐", "🥳", "🎈",
        "🍰", "🍪", "🍩", "🍕", "🎯",
    ],
    "uncommon": [
        "🌟", "💫", "🚀", "🔥", "⚡",
        "🍀", "🎆", "🎇",
    ],
    "rare": [
        "🏆", "💎", "🦄", "🤖", "🌈",
    ],
    "epic": [
        "👑", "🐉", "🌌", "☄️",
    ],
    "legendary": [
        "🪩", "🌠", "🧙", "🦖",
    ],
}

# Probability weights
EMOJI_WEIGHTS = {
    "common": 60,
    "uncommon": 25,
    "rare": 10,
    "epic": 4,
    "legendary": 1,
}


MESSAGES = {
    "common": [
        "Great work!",
        "Nicely done!",
        "Success!",
        "Looking good!",
        "Tests passed!",
        "Forward!",
        "Another milestone reached!",
    ],
    "uncommon": [
        "Excellent craftsmanship!",
        "Code approved!",
        "Progress achieved!",
        "Another bug falls.",
        "Elegant work.",
    ],
    "rare": [
        "The interpreter smiles upon you.",
        "The Python spirits are pleased.",
        "You have gained experience.",
    ],
    "epic": [
        "The compiler gods are impressed.",
        "A beautiful solution emerges.",
    ],
    "legendary": [
        "Guido nods approvingly.",
        "You have written acceptable Python.",
    ],
}

MESSAGE_WEIGHTS = {
    "common": 75,
    "uncommon": 18,
    "rare": 5,
    "epic": 1.7,
    "legendary": 0.3,
}


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def _project_seed(directory: Path = Path(".")) -> int:
    """Return a deterministic seed based on the AST of every Python file."""

    digest = hashlib.sha256()

    for path in sorted(directory.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue

        try:
            source = path.read_text(encoding="utf8")
            tree = ast.parse(source)

            canonical = ast.dump(
                tree,
                annotate_fields=False,
                include_attributes=False,
            )

            digest.update(path.as_posix().encode())
            digest.update(canonical.encode())

        except Exception:
            digest.update(path.read_bytes())

    return int.from_bytes(digest.digest()[:8], "big")


# ---------------------------------------------------------------------------
# Random helpers
# ---------------------------------------------------------------------------

def _weighted_choice(rng: random.Random, table: dict):
    """Choose one rarity according to its weights."""
    rarities = list(table)
    weights = [table[r] for r in rarities]
    return rng.choices(rarities, weights=weights, k=1)[0]


def _random_emoji(rng: random.Random) -> str:
    rarity = _weighted_choice(rng, EMOJI_WEIGHTS)
    return rng.choice(EMOJIS[rarity])


def _random_message(rng: random.Random) -> str:
    rarity = _weighted_choice(rng, MESSAGE_WEIGHTS)
    return rng.choice(MESSAGES[rarity])


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def celebrate(task: str | None = None) -> None:
    """
    Return a deterministic celebration string.

    Example:
        >>> celebration("2.3")
        'Task 2.3 complete! Great work! 🎉 🍕 ⭐'
    """

    rng = random.Random(_project_seed())

    message = _random_message(rng)

    # Roll 3–5 emoji independently.
    emojis = " ".join(
        _random_emoji(rng)
        for _ in range(rng.randint(3, 5))
    )

    # if task is None:
    #     return f"{message} {emojis}"

    print(f"Task {task} complete! {message} {emojis}")