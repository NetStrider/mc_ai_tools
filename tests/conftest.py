import sys
from pathlib import Path


def pytest_configure():  # pragma: no cover - test harness utility
    root = Path(__file__).resolve().parent.parent / "src"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
