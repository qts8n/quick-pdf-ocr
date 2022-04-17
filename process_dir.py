import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import os.path as osp

import easyocr
import fitz
from tqdm import tqdm

import docs
import utils

_OUT_DIR_PATH = 'outputs'


def document_to_content(document, reader):
    content = []
    for page in document:
        content.append(docs.page_to_content(page, reader))
    return ' '.join(content)


def _main(config_dto):
    reader = easyocr.Reader(['ru'], gpu=True)
    pdf_paths = utils.get_pdf_paths(config_dto.dir_path)
    for pdf_path in tqdm(pdf_paths, desc='Processing documents'):
        pdf_name, _ = osp.splitext(osp.basename(pdf_path))
        output_path = osp.join(config_dto.out_dir_path, f'{pdf_name}.txt')
        if osp.isfile(output_path):
            continue
        document = fitz.open(pdf_path)
        content = document_to_content(document, reader)
        with open(output_path, 'w+') as o_file:
            o_file.writelines(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a whole directory of PDFs through the OCR')
    parser.add_argument(
        '-d', '--dir-path',
        type=utils.dir_path_type,
        required=True,
        help='PDF directory path')
    parser.add_argument(
        '-o', '--out-dir-path',
        type=utils.dir_path_type,
        default=_OUT_DIR_PATH,
        help='Output directory path')
    args = parser.parse_args()
    _main(args)
