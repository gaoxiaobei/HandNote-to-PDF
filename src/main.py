# HandNote-to-PDF/src/main.py

from preprocessing import load_image, to_grayscale, apply_binary_threshold, reduce_noise
from vectorization import find_contours, contours_to_svg
from pdf_integration import overlay_svg_on_pdf
from create_dummy_image import create_dummy_image
from create_dummy_pdf import create_dummy_pdf

def main():
    """Main function to run the full pipeline."""
    # Define file paths
    input_image_path = 'data/dummy_note.png'
    input_pdf_path = 'data/dummy_document.pdf'
    output_svg_path = 'output/dummy_note.svg'
    output_pdf_path = 'output/final_document.pdf'
    
    # Create dummy files for testing
    create_dummy_image(input_image_path)
    create_dummy_pdf(input_pdf_path)
    
    # Load the image
    image = load_image(input_image_path)
    
    # Preprocess the image
    grayscale_image = to_grayscale(image)
    binary_image = apply_binary_threshold(grayscale_image)
    denoised_image = reduce_noise(binary_image)
    
    # Find contours
    contours = find_contours(denoised_image)
    
    # Convert contours to SVG
    height, width, _ = image.shape
    contours_to_svg(contours, width, height, output_svg_path)
    
    # Overlay the SVG on the PDF
    overlay_svg_on_pdf(input_pdf_path, output_svg_path, output_pdf_path)
    
    print(f"Successfully created final PDF with vectorized notes at {output_pdf_path}")

if __name__ == "__main__":
    main()
