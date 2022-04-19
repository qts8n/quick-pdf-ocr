import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import multiprocessing
import os.path as osp
from time import perf_counter
import re

import easyocr
import fitz

import docs
import utils

_OUT_DIR_PATH = 'outputs'
_STRIP_REGEXP = r'(\n|\r| )+'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


def document_to_content(document, reader):
    content = []
    for page in document:
        page_content = re.sub(_STRIP_REGEXP, ' ', page.get_text()).strip()
        if not page_content:
            page_content = docs.page_to_content(page, reader)
        content.append(page_content)
    return ' '.join(content)


def _main(config_dto):
    reader = easyocr.Reader(['ru'], gpu=True)
    pdf_paths = utils.get_pdf_paths(config_dto.dir_path)
    logger.info('INFO: Model has been initialized. Processing documents...')
    doc_num = len(pdf_paths)
    for doc_idx, pdf_path in enumerate(pdf_paths, start=1):
        pdf_name, _ = osp.splitext(osp.basename(pdf_path))
        output_path = osp.join(config_dto.out_dir_path, f'{pdf_name}.txt')
        if osp.isfile(output_path):
            logger.info('WARN: Document "%s" was already processed before', pdf_name)
            continue
        document = fitz.open(pdf_path)
        logger.info('INFO: Processing document "%s" (%i pages) [%i/%i]', pdf_name, len(document), doc_idx, doc_num)
        t_start = perf_counter()
        content = document_to_content(document, reader)
        t_end = perf_counter()
        logger.info('INFO: Document "%s" has been processed successfully! (time: %fs)', pdf_name, t_end - t_start)
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
