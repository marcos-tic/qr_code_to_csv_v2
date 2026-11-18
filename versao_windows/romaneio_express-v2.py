"""Launcher compatível com a antiga distribuição Windows do Romaneio Express V2."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from romaneio_express_v2 import *  # noqa: E402,F401,F403

if __name__ == "__main__":
    main()
