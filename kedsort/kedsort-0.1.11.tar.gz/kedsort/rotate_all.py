import PyPDF2
import sys

def rotate_all(input_pdf, output_pdf, degrees):
    pdf_in = open(input_pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in, False)
    pdf_writer = PyPDF2.PdfFileWriter()
    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        page.rotateClockwise(degrees)
        pdf_writer.addPage(page)
    pdf_out = open(output_pdf, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
