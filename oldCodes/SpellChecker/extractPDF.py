#Script to extract text from pdf file "Files/ti-prins.pdf"
from PyPDF2 import PdfFileReader

pdf = PdfFileReader("Files/ti-prins.pdf")

# print(pdf.getNumPages())
# first_page = pdf.getPage(1)
# text = first_page.extractText()
# print(text)

with open('Files/big.txt',mode="a") as fw:
    for page in pdf.pages:
        text = page.extractText()
        fw.write(text)