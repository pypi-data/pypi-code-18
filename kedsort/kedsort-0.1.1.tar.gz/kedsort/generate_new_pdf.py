import click
import PyPDF2
import sys
from list_numbers import list_numbers

def generate_new_pdf(input_pdf, pages_list, output_pdf):
    ''' Create a new pdf from a given list of pages '''
    pages_list = list_numbers(pages_list)
    pdf_in = open(input_pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()
    for index in range(pdf_reader.numPages):
        new_page = pdf_reader.getPage(index)
        if index in pages_list:
            new_page = pdf_reader.getPage(index)
            string = "added page: " + str(index+1)
            pdf_writer.addPage(new_page)
            click.secho(string, fg='blue')

    pdf_out = open(output_pdf, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
