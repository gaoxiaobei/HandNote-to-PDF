# HandNote-to-PDF/src/main.py

import argparse
import os
import sys
from preprocessing import load_image, correct_perspective, to_grayscale, apply_adaptive_threshold, reduce_noise, apply_binary_threshold
from vectorization import find_contours, contours_to_svg
from pdf_integration import overlay_svg_on_pdf

def validate_input_files(image_path, pdf_path):
    """Validate that input files exist and are of correct types."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Check file extensions
    if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError(f"Unsupported image format. Supported formats: PNG, JPG, JPEG")
    
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"Unsupported PDF format. File must have .pdf extension")

def main():
    """Main function to run the full pipeline with command-line arguments."""
    try:
        # Set up argument parser
        parser = argparse.ArgumentParser(description="Convert handwritten notes on a PDF to a new PDF with vectorized annotations.")
        parser.add_argument("--image", required=True, help="Path to the input image file with handwritten notes.")
        parser.add_argument("--pdf", required=True, help="Path to the original PDF file.")
        parser.add_argument("--output", required=True, help="Path to the output PDF file.")
        parser.add_argument("--threshold", type=int, default=None, help="Threshold value for binary thresholding (0-255). If not provided, adaptive thresholding is used.")
        parser.add_argument("--no-perspective", action="store_true", help="Skip perspective correction step.")
        parser.add_argument("--noise-reduction", type=int, default=5, help="Noise reduction strength (odd number, default: 5).")
        args = parser.parse_args()

        # Define file paths
        input_image_path = args.image
        input_pdf_path = args.pdf
        output_pdf_path = args.output
        
        # Validate input files
        validate_input_files(input_image_path, input_pdf_path)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_pdf_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Define a temporary path for the SVG file
        temp_svg_path = os.path.join(output_dir, "temp.svg") if output_dir else "temp.svg"

        # Load the image
        print("Loading image...")
        image = load_image(input_image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {input_image_path}")
        
        # Correct the perspective (if requested)
        if not args.no_perspective:
            print("Correcting perspective...")
            corrected_image = correct_perspective(image)
        else:
            print("Skipping perspective correction...")
            corrected_image = image
        
        # Preprocess the image
        print("Preprocessing image...")
        grayscale_image = to_grayscale(corrected_image)
        
        # Apply thresholding (binary or adaptive)
        if args.threshold is not None:
            print(f"Applying binary threshold with value {args.threshold}...")
            binary_image = apply_binary_threshold(grayscale_image, args.threshold)
        else:
            print("Applying adaptive threshold...")
            binary_image = apply_adaptive_threshold(grayscale_image)
        
        # Apply noise reduction
        if args.noise_reduction > 0:
            print(f"Reducing noise with strength {args.noise_reduction}...")
            # Ensure noise reduction value is odd
            noise_reduction = args.noise_reduction if args.noise_reduction % 2 == 1 else args.noise_reduction + 1
            denoised_image = reduce_noise(binary_image, noise_reduction)
        else:
            print("Skipping noise reduction...")
            denoised_image = binary_image
        
        # Find contours
        print("Finding contours...")
        contours = find_contours(denoised_image)
        
        # Convert contours to SVG
        print("Converting to SVG...")
        height, width = corrected_image.shape[:2]
        contours_to_svg(contours, width, height, temp_svg_path)
        
        # Overlay the SVG on the PDF
        print("Overlaying SVG on PDF...")
        overlay_svg_on_pdf(input_pdf_path, temp_svg_path, output_pdf_path)
        
        # Clean up the temporary SVG file
        if os.path.exists(temp_svg_path):
            os.remove(temp_svg_path)
        
        print(f"Successfully created final PDF with vectorized notes at {output_pdf_path}")
        
    except FileNotFoundError as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Value error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
