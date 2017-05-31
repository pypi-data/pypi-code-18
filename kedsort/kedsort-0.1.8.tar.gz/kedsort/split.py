import click
import os
import PyPDF2

def split_pure_python(pdf, first_page, last_page, outputpdf):
    pdf_in = open(pdf, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()
    for page in range(first_page - 1, last_page):
        new_page = pdf_reader.getPage(page)
        pdf_writer.addPage(new_page)

    pdf_out = open(outputpdf, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
    string = "Created " + outputpdf
    click.secho(string, fg='blue')

def loop_scripts(pdf, start_page, total_pages, increment, outputpdf):
    current_page = start_page
    for index in range(start_page, total_pages+1):
        if (current_page < total_pages):
            pdfName = outputpdf.replace(".pdf", "") + "-" + str(index) + ".pdf"
            last_page = current_page + increment - 1
            if last_page > total_pages:
                last_page = total_pages
            split_pure_python(pdf, current_page, last_page, pdfName)
            current_page = current_page + increment
