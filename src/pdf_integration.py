import fitz  # PyMuPDF
import os
import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

def overlay_svg_on_pdf(original_pdf_path, svg_path, output_pdf_path):
    """
    Overlays an SVG image onto the first page of a PDF document by converting
    the SVG to a temporary PDF and stamping it onto the original.
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_pdf_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Check if input files exist
        if not os.path.exists(original_pdf_path):
            raise FileNotFoundError(f"Original PDF file not found: {original_pdf_path}")
        
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"SVG file not found: {svg_path}")
        
        # Define a temporary path for the PDF overlay
        temp_pdf_path = os.path.join(output_dir, "temp_overlay.pdf") if output_dir else "temp_overlay.pdf"

        # 1. Convert SVG to a temporary PDF with a transparent background
        print("Converting SVG to PDF...")
        drawing = svg2rlg(svg_path)
        
        # Get original PDF dimensions to match page size
        print("Reading original PDF...")
        original_pdf_doc = fitz.open(original_pdf_path)
        page_rect = original_pdf_doc[0].rect
        page_width, page_height = page_rect.width, page_rect.height
        
        c = canvas.Canvas(temp_pdf_path, pagesize=(page_width, page_height))
        renderPDF.draw(drawing, c, 0, 0)
        c.save()

        # 2. Open the temporary overlay PDF
        print("Opening overlay PDF...")
        overlay_pdf = fitz.open(temp_pdf_path)
        
        # 3. Get the first page of the original PDF and stamp the overlay
        print("Overlaying PDFs...")
        first_page = original_pdf_doc[0]
        first_page.show_pdf_page(first_page.rect, overlay_pdf, 0)
        
        # 4. Save the new PDF
        print("Saving final PDF...")
        original_pdf_doc.save(output_pdf_path)
        
        # 5. Close documents and clean up
        original_pdf_doc.close()
        overlay_pdf.close()
        
        # Clean up temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
            
    except FileNotFoundError as e:
        print(f"File error: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Error in PDF overlay process: {e}", file=sys.stderr)
        # Clean up any temporary files if they exist
        if 'temp_pdf_path' in locals() and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        raise
