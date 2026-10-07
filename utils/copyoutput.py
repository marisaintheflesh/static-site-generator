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



def copy_directory_tree(src_dir, tar_dir):
    """
    Manually copies all files and folders recursively from source to target.
    Recreates directories and preserves file metadata using shutil.copy2.
    """
    src = Path(src_dir)
    dst = Path(tar_dir)

    for item in src.rglob("*"):
        relative_path = item.relative_to(src)
        target_item = dst / relative_path

        if item.is_dir():
            target_item.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target_item.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target_item)


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
    copy_directory_tree(output, target)


if __name__ == "__main__":
    main()
