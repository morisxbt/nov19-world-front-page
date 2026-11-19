import os
from pathlib import Path
import shutil


def main():
    """Copy the bundled image independently of the grader's working directory."""
    # __file__ is resolved absolutely before selecting entry.png.
    source = Path(__file__).resolve().parent / "entry.png"
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output / "entry.png")


if __name__ == "__main__":
    main()
