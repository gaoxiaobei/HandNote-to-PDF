# HandNote-to-PDF/src/main.py

import argparse
import os
from preprocessing import load_image, to_grayscale, apply_adaptive_threshold, reduce_noise
from vectorization import find_contours, contours_to_svg
from pdf_integration import overlay_svg_on_pdf

def main():
    """Main function to run the full pipeline with command-line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert handwritten notes on a PDF to a new PDF with vectorized annotations.")
    parser.add_argument("--image", required=True, help="Path to the input image file with handwritten notes.")
    parser.add_argument("--pdf", required=True, help="Path to the original PDF file.")
    parser.add_argument("--output", required=True, help="Path to the output PDF file.")
    args = parser.parse_args()

    # Define file paths
    input_image_path = args.image
    input_pdf_path = args.pdf
    output_pdf_path = args.output
    
    # Define a temporary path for the SVG file
    output_dir = os.path.dirname(output_pdf_path)
    temp_svg_path = os.path.join(output_dir, "temp.svg")

    # Load the image
    image = load_image(input_image_path)
    
    # Preprocess the image
    grayscale_image = to_grayscale(image)
    binary_image = apply_adaptive_threshold(grayscale_image)
    denoised_image = reduce_noise(binary_image)
    
    # Find contours
    contours = find_contours(denoised_image)
    
    # Convert contours to SVG
    height, width, _ = image.shape
    contours_to_svg(contours, width, height, temp_svg_path)
    
    # Overlay the SVG on the PDF
    overlay_svg_on_pdf(input_pdf_path, temp_svg_path, output_pdf_path)
    
    # Clean up the temporary SVG file
    os.remove(temp_svg_path)
    
    print(f"Successfully created final PDF with vectorized notes at {output_pdf_path}")

if __name__ == "__main__":
    main()
