import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent # get parent directory of "utils" directory
output = root / "__site"

target = "/var/www/sites/1r1s.gg/"

def clear_directory(dir_path):
    target_dir = Path(dir_path)

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Directory {dir_path} does not exist.")
        return

    for item in target_dir.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def main():
    if not Path(root).exists():
        print(f"Script Parent Directory: {root} directory doesn't exist.")

    if not Path(output).exists():
        print(f"Source Directory: {output} directory doesn't exist.")
        return

    if not Path(target).exists():
        print(f"Target Directory: {target} directory doesn't exist.")
        return

    clear_directory(target)

    shutil.copytree(output, target)


if __name__ == "__main__":
    main()
