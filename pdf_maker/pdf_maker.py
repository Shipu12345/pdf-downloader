import os
from PIL import Image
from fpdf import FPDF

def create_optimized_pdf(image_paths, output_pdf):
    pdf = FPDF()
    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, x=10, y=10, w=190)
    pdf.output(output_pdf, "F")


def make_pdf(pdf_name, image_paths, download_folder):
    print("Converting image paths to PDF...")
    pdf_filename = f'{pdf_name}.pdf'
    pdf_filepath = f'./data/complete_pdfs/{pdf_filename}'

    create_optimized_pdf(image_paths, pdf_filepath)
    
    print(f'PDF created: {pdf_filename}')
    print(f'Total images downloaded: {len(image_paths)}')
    
    for img_path in image_paths:
        os.remove(img_path)
    os.rmdir(download_folder)
