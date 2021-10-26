import os
from enum import Enum
from typing import Optional
from shutil import copy, rmtree
import ntpath


class ImageExtension(str, Enum):
    JPG = '.jpg'
    JPEG = '.jpeg'
    PNG = '.png'


def get_image_extension(file: str) -> Optional[ImageExtension]:
    ext = os.path.splitext(file)[1].lower()
    try:
        return ImageExtension(ext)
    except ValueError:
        return None


def get_image_name(file: str) -> str:
    head, tail = ntpath.split(file)
    return tail or ntpath.basename(head)


def get_parent_path(file: str) -> str:
    from pathlib import Path
    path = Path(file)
    return path.parent.absolute()


def copy_image(file: str, dir: str):
    copy(file, dir)


def create_dir(dir: str):
    if not os.path.exists(dir):
        os.mkdir(dir)


def remove_dir(dir: str):
    if os.path.exists(dir):
        rmtree(dir)
