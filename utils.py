import os
import subprocess

from pathlib import Path

FILE_ROOT = Path(__file__).parent
ROOT_DIR = FILE_ROOT.parent
DATA_DIR = FILE_ROOT / "data"
GAF_DIR = ROOT_DIR / "gaf"
GFF_DIR = ROOT_DIR / "gff"
GTF_DIR = ROOT_DIR / "gtf"


def rg_search(path: Path, pattern: str) -> list[str]:
    os.chdir(path)
    return subprocess.run(
        ["rg", pattern], capture_output=True, text=True
    ).stdout.splitlines()
