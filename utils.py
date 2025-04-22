import os
import subprocess

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
GAF_DIR = ROOT_DIR / "gaf"
GFF_DIR = ROOT_DIR / "gff"


def rg_search(path: Path, pattern: str) -> list[str]:
    os.chdir(path)
    return subprocess.run(
        ["rg", pattern], capture_output=True, text=True
    ).stdout.splitlines()
