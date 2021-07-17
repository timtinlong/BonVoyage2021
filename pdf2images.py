''' https://stackoverflow.com/questions/45795089/how-can-i-read-pdf-in-python '''
''' https://stackoverflow.com/questions/11087795/whitespace-gone-from-pdf-extraction-and-strange-word-interpretation/11087993 '''

''' Using pdfminer's documentation: https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html '''

''' https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python '''

from io import StringIO
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import fitz

# class to convert the pdf to Python variable or save as a .txt file
class PdfConverter:
    def __init__(self, path, fn):
        self.path=path
        self.fn=fn
        self.filePath=os.path.join(path, 'PDF', fn)
        self.savePath=os.path.join(path, 'outputs')
        self.savePathPDFPages=os.path.join(path, 'RawPages')

        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)

        if not os.path.exists(self.savePathPDFPages):
            os.makedirs(self.savePathPDFPages)

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

                    txt_pdf = open(os.path.join(self.savePath, 'p-'+str(pageNumber)+'-'+self.fn[:-4]+'.txt'), 'wb')
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

    def extractFigures(self):
        doc = fitz.open(self.filePath)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG(os.path.join(self.savePath, "p%s-%s.png" % (i, xref)))
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(os.path.join(self.savePath, "p%s-%s.png" % (i, xref)))
                    pix1 = None
                pix = None

    def pages2Images(self):
        doc = fitz.open(self.filePath)
        
        for i in range(len(doc)):
            page = doc.loadPage(i)  # number of page
            pix = page.getPixmap()
            output = os.path.join(self.savePathPDFPages, str(i)+"-"+self.fn[:-4]+".png")
            pix.writePNG(output)

if __name__ == '__main__':
    
    path = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(os.path.join(path, 'PDF')):
        if file.endswith(".pdf"):
            print('processing:', file)
            fn = file
            if fn[-3:] != 'pdf':
                raise Exception('ERROR: not a PDF file')

            verbose = 0
            pdfConverter = PdfConverter(path=path, fn=fn)
            if verbose: print(pdfConverter.pdf2var(savePathBool=False))
            if verbose: print(pdfConverter.pdf2var(savePathBool=True))
            # pdfConverter.extractFigures()
            pdfConverter.pages2Images()


