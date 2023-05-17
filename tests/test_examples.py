from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize('path', (ROOT / 'examples').iterdir())
def test_example(path: Path) -> None:
    cmd = [sys.executable, str(path)]
    res = subprocess.run(cmd)
    res.check_returncode()
