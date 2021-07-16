''' https://stackoverflow.com/questions/45795089/how-can-i-read-pdf-in-python '''
''' https://stackoverflow.com/questions/11087795/whitespace-gone-from-pdf-extraction-and-strange-word-interpretation/11087993 '''

''' Using pdfminer's documentation: https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html '''

from io import StringIO
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# class to convert the pdf to Python variable or save as a .txt file
class PdfConverter:
    def __init__(self, path, fn):
        self.path=path
        self.fn=fn
        self.filePath = os.path.join(path, fn)

    def pdf2var(self, savePathBool):
        # from the documentation: https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html
        output_string = StringIO()
        with open(self.filePath, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for pageNumber, page in enumerate(PDFPage.create_pages(doc)):
                if savePathBool:
                    # if true, we restart each page and save each page as a .txt file
                    output_string_page = StringIO()
                    rsrcmgr_page = PDFResourceManager()
                    device_page = TextConverter(rsrcmgr_page, output_string_page, laparams=LAParams())
                    interpreter_page = PDFPageInterpreter(rsrcmgr_page, device_page)
                    interpreter_page.process_page(page)
                    pContent = output_string_page.getvalue()

                    txt_pdf = open(os.path.join(self.path, 'p-'+str(pageNumber)+'-'+self.fn[:-4]+'.txt'), 'wb')
                    txt_pdf.write(pContent.encode('utf-8'))
                    txt_pdf.close()
                    interpreter.process_page(page)

                else:
                    interpreter.process_page(page)

        return output_string.getvalue()

    def pdf2txt(self):
        # saving the variable as a .txt
        content = self.pdf2var(savePathBool=True)
        return content

if __name__ == '__main__':
    
    path = os.path.dirname(os.path.abspath(__file__))
    fn = 'CycleGAN.pdf'

    if fn[-3:] != 'pdf':
        raise Exception('ERROR: not a PDF file')
    verbose = 1

    pdfConverter = PdfConverter(path=path, fn=fn)
    if verbose: print(pdfConverter.pdf2var(savePathBool=False))
    if verbose: print(pdfConverter.pdf2var(savePathBool=True))

