"""Launcher do aplicativo Windows usando a implementação compartilhada."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main_windows import *  # noqa: E402,F401,F403

if __name__ == "__main__":
    main()
