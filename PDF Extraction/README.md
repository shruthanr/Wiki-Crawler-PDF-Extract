# PDF Extractor
Python programs to extract text from pdfs. 
- `extract_all.py`: Extracts content from all the pdfs in the Google Sheet
- `extract_single.py`: Extracts content from the specified pdf. The pdf can be specified either by mentioning the url to the pdf (`--url=="..."`) or by mentioning the row number in the Google Sheet (`--row_num=2`)

### Requirements
- `requests`
- `tesseract`
- `poppler`
- `pytesseract`
- `bs4` (Beautiful Soup)
- `pdf2image`
- `pandas`
- `argparse`

### Approach
The programs use `pdf2image` to convert the pdf to an image. Then `tesseract` is used to perform OCR to extract the content. The language is set to `hin` (which also follows the Devanagari script). In case the URL is not a downloadable pdf, then BeautifulSoup is used to identify all links in the page which contain ".pdf". 
