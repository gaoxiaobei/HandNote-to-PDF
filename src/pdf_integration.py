import fitz  # PyMuPDF
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

def overlay_svg_on_pdf(original_pdf_path, svg_path, output_pdf_path):
    """
    Overlays an SVG image onto the first page of a PDF document by converting
    the SVG to a temporary PDF and stamping it onto the original.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    # Define a temporary path for the PDF overlay
    temp_pdf_path = os.path.join(os.path.dirname(output_pdf_path), "temp_overlay.pdf")

    # 1. Convert SVG to a temporary PDF with a transparent background
    drawing = svg2rlg(svg_path)
    
    # Get original PDF dimensions to match page size
    original_pdf_doc = fitz.open(original_pdf_path)
    page_rect = original_pdf_doc[0].rect
    page_width, page_height = page_rect.width, page_rect.height
    
    c = canvas.Canvas(temp_pdf_path, pagesize=(page_width, page_height))
    renderPDF.draw(drawing, c, 0, 0)
    c.save()

    # 2. Open the temporary overlay PDF
    overlay_pdf = fitz.open(temp_pdf_path)
    
    # 3. Get the first page of the original PDF and stamp the overlay
    first_page = original_pdf_doc[0]
    first_page.show_pdf_page(first_page.rect, overlay_pdf, 0)
    
    # 4. Save the new PDF
    original_pdf_doc.save(output_pdf_path)
    
    # 5. Close documents and clean up
    original_pdf_doc.close()
    overlay_pdf.close()
    os.remove(temp_pdf_path)
