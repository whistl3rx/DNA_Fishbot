"""
Duet Night Abyss - Auto Fishing minigame bot (refactored)

This module was refactored into an OOP structure without changing behavior.
All user-facing strings and comments were translated to English.
"""
"""Launcher for the refactored Duet Night Abyss auto-fishing bot.

This file now only composes the `FishingBot` and starts it.
"""

from pathlib import Path

from src.bot import FishingBot


if __name__ == "__main__":
    base = Path(__file__).parent
    bot = FishingBot(base)
    bot.run()