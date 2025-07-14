from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_pdf(file_path):
    """Creates a simple dummy PDF file."""
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    c.drawString(72, height - 72, "This is a dummy PDF for testing.")
    c.drawString(72, height - 144, "The vectorized handwriting will be overlaid on this document.")
    
    c.save()

if __name__ == '__main__':
    create_dummy_pdf('data/dummy_document.pdf')
