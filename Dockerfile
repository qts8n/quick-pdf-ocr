FROM challisa/easyocr:latest

RUN pip install --no-cache-dir PyMuPDF

COPY . /workspace
