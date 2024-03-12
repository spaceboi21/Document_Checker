# Document Checker Web Application

## Description
This Flask application allows users to upload documents and perform Optical Character Recognition (OCR) to extract text from them. It then searches for specific strings such as names, CNIC numbers, or passport numbers within the extracted text and provides feedback on whether these strings were found in the document.

## Requirements
- Python 3.x
- Flask
- Doctr

## Installation
1. Install Python 3.x if not already installed.
2. Install Flask and Doctr using pip:
   ```bash
   pip install flask
   pip install python-doctr
   pip install "python-doctr[tf]"
   pip install "python-doctr[torch]"# WeAlif_doc_check
