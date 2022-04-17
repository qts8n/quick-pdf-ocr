FROM challisa/easyocr:latest

RUN pip install --no-cache-dir PyMuPDF && pip install --no-cache-dir --upgrade easyocr

COPY . /workspace
