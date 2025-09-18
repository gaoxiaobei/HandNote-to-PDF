# HandNote-to-PDF/src/batch_process.py

import argparse
import os
import sys
from main import validate_input_files
from preprocessing import load_image, correct_perspective, to_grayscale, apply_adaptive_threshold, reduce_noise
from vectorization import find_contours, contours_to_svg
from pdf_integration import overlay_svg_on_pdf

def process_single_image(image_path, pdf_path, output_path, threshold=None, no_perspective=False, noise_reduction=5):
    """Process a single image with the HandNote-to-PDF pipeline."""
    try:
        print(f"Processing {image_path}...")
        
        # Validate input files
        validate_input_files(image_path, pdf_path)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Define a temporary path for the SVG file
        temp_svg_path = os.path.join(output_dir, "temp.svg") if output_dir else "temp.svg"

        # Load the image
        print("  Loading image...")
        image = load_image(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Correct the perspective (if requested)
        if not no_perspective:
            print("  Correcting perspective...")
            corrected_image = correct_perspective(image)
        else:
            print("  Skipping perspective correction...")
            corrected_image = image
        
        # Preprocess the image
        print("  Preprocessing image...")
        grayscale_image = to_grayscale(corrected_image)
        
        # Apply thresholding (binary or adaptive)
        if threshold is not None:
            print(f"  Applying binary threshold with value {threshold}...")
            from preprocessing import apply_binary_threshold
            binary_image = apply_binary_threshold(grayscale_image, threshold)
        else:
            print("  Applying adaptive threshold...")
            binary_image = apply_adaptive_threshold(grayscale_image)
        
        # Apply noise reduction
        if noise_reduction > 0:
            print(f"  Reducing noise with strength {noise_reduction}...")
            # Ensure noise reduction value is odd
            noise_reduction = noise_reduction if noise_reduction % 2 == 1 else noise_reduction + 1
            denoised_image = reduce_noise(binary_image, noise_reduction)
        else:
            print("  Skipping noise reduction...")
            denoised_image = binary_image
        
        # Find contours
        print("  Finding contours...")
        contours = find_contours(denoised_image)
        
        # Convert contours to SVG
        print("  Converting to SVG...")
        height, width = corrected_image.shape[:2]
        contours_to_svg(contours, width, height, temp_svg_path)
        
        # Overlay the SVG on the PDF
        print("  Overlaying SVG on PDF...")
        overlay_svg_on_pdf(pdf_path, temp_svg_path, output_path)
        
        # Clean up the temporary SVG file
        if os.path.exists(temp_svg_path):
            os.remove(temp_svg_path)
        
        print(f"  Successfully created {output_path}")
        return True
        
    except Exception as e:
        print(f"  Error processing {image_path}: {e}", file=sys.stderr)
        return False

def main():
    """Main function to process multiple images."""
    parser = argparse.ArgumentParser(description="Batch process multiple handwritten note images.")
    parser.add_argument("--images", nargs='+', required=True, help="Paths to the input image files with handwritten notes.")
    parser.add_argument("--pdf", required=True, help="Path to the original PDF file.")
    parser.add_argument("--output-dir", required=True, help="Directory to save output PDF files.")
    parser.add_argument("--threshold", type=int, default=None, help="Threshold value for binary thresholding (0-255). If not provided, adaptive thresholding is used.")
    parser.add_argument("--no-perspective", action="store_true", help="Skip perspective correction step.")
    parser.add_argument("--noise-reduction", type=int, default=5, help="Noise reduction strength (odd number, default: 5).")
    args = parser.parse_args()

    # Validate PDF file
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)
    
    if not args.pdf.lower().endswith('.pdf'):
        print(f"Error: Unsupported PDF format. File must have .pdf extension", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Process each image
    success_count = 0
    total_count = len(args.images)
    
    for image_path in args.images:
        # Generate output path
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(args.output_dir, f"{image_name}_output.pdf")
        
        # Process the image
        if process_single_image(
            image_path, 
            args.pdf, 
            output_path, 
            args.threshold, 
            args.no_perspective, 
            args.noise_reduction
        ):
            success_count += 1

    print(f"\nBatch processing complete: {success_count}/{total_count} images processed successfully.")

if __name__ == "__main__":
    main()