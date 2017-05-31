import click
import PyPDF2
import sys
from list_numbers import list_numbers

def rotate_pages_by_degrees(pdf, pages_list, output_pdf, clockwise_rotation_in_degrees):
    pages_list = list_numbers(pages_list)
    pdf_in = open(pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()
    for index in range(pdf_reader.numPages):
        new_page = pdf_reader.getPage(index)
        if index in pages_list:
            new_page = pdf_reader.getPage(index)
            string = "rotated page: " + str(index + 1) + " " + str(clockwise_rotation_in_degrees) + " degrees"
            new_page.rotateClockwise(clockwise_rotation_in_degrees)
            click.secho(string, fg='blue')
        pdf_writer.addPage(new_page)
    pdf_out = open(output_pdf, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
