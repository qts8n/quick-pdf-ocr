import argparse
from glob import glob
import os.path as osp

import cv2

_PDF_EXTENSIONS = [
    '*.pdf',
    '*.PDF',
    '*.pdfa',
    '*.PDFA',
]


def _get_paths(root_dir: str, extensions: list) -> list:
    paths = []
    for ext in extensions:
        glob_str = osp.join(root_dir, ext)
        paths.extend(glob(glob_str, recursive=True))
    return sorted(paths)


def get_pdf_paths(root_dir: str) -> list:
    return _get_paths(root_dir, _PDF_EXTENSIONS)


def dir_path_type(path: str) -> str:
    if osp.isdir(path):
        return osp.abspath(osp.realpath(path))
    else:
        raise argparse.ArgumentTypeError(
            f'{path} is not a valid directory path')
