from pathlib import Path
from shutil import move


def is_existing_directory(directory: Path):
    return directory.exists() and directory.is_dir()


def ensure_is_existing_directory(directory: Path):
    if not is_existing_directory(directory):
        raise NotADirectoryError(str(directory) + " is not a dir")


def list_only_dirs(directory: Path):
    ensure_is_existing_directory(directory)
    return [item for item in directory.iterdir() if item.is_dir()]


def list_only_files(directory: Path):
    ensure_is_existing_directory(directory)
    return [item for item in directory.iterdir() if not item.is_dir()]


def list_content(directory: Path):
    ensure_is_existing_directory(directory)
    return list_only_dirs(directory) + list_only_files(directory)


def list_dirs_recursively(directory: Path):
    ensure_is_existing_directory(directory)

    found_dirs = []
    for item in directory.iterdir():
        if item.is_dir():
            found_dirs.append(item)
            found_dirs += list_dirs_recursively(item)

    return found_dirs


def list_files_recursively(directory: Path):
    ensure_is_existing_directory(directory)

    found_files = list_only_files(directory)
    found_dirs = list_only_dirs(directory)

    for dir in found_dirs:
        found_files += list_files_recursively(dir)

    return found_files


def list_all_dir_content_recursively(directory: Path):
    ensure_is_existing_directory(directory)

    return list_files_recursively(directory) + list_dirs_recursively(directory)


def move_all_files(source_dir: Path, target_dir: Path):
    ensure_is_existing_directory(source_dir)

    if not is_existing_directory(target_dir):
        target_dir.mkdir(parents=True)

    all_files_from_dir = [file.relative_to(source_dir) for file in list_only_files(source_dir)]
    for file in all_files_from_dir:
        move(source_dir / file, target_dir / file)


def move_all_content(source_dir: Path, target_dir: Path):
    ensure_is_existing_directory(source_dir)
    if not is_existing_directory(target_dir):
        target_dir.mkdir(parents=True)

    all_content_from_dir = [file.relative_to(source_dir) for file in list_content(source_dir)]
    for content in all_content_from_dir:
        move(source_dir / content, target_dir / content)
