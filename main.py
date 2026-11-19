import os
from pathlib import Path
import shutil


def main():
    """Copy the image next to this file, regardless of the grader's cwd."""
    # Resolve the script path before locating the bundled image.
    source = Path(__file__).resolve().parent / "entry.png"
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output / "entry.png")


if __name__ == "__main__":
    main()
