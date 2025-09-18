# HandNote-to-PDF/src/gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import threading
from main import validate_input_files
from preprocessing import load_image, correct_perspective, to_grayscale, apply_adaptive_threshold, reduce_noise
from vectorization import find_contours, contours_to_svg
from pdf_integration import overlay_svg_on_pdf

class HandNoteToPDFGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HandNote-to-PDF")
        self.root.geometry("600x500")
        
        # Variables
        self.image_path = tk.StringVar()
        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.threshold_value = tk.StringVar(value="")
        self.no_perspective = tk.BooleanVar()
        self.noise_reduction = tk.StringVar(value="5")
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="HandNote-to-PDF", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Image selection
        ttk.Label(main_frame, text="Image File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.image_path).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="Browse...", command=self.browse_image).grid(row=1, column=2, pady=5)
        
        # PDF selection
        ttk.Label(main_frame, text="PDF File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.pdf_path).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="Browse...", command=self.browse_pdf).grid(row=2, column=2, pady=5)
        
        # Output selection
        ttk.Label(main_frame, text="Output File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="Browse...", command=self.browse_output).grid(row=3, column=2, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Threshold option
        ttk.Label(options_frame, text="Threshold Value:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(options_frame, textvariable=self.threshold_value, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(options_frame, text="(Leave empty for adaptive thresholding)").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Perspective correction option
        ttk.Checkbutton(options_frame, text="Skip Perspective Correction", variable=self.no_perspective).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Noise reduction option
        ttk.Label(options_frame, text="Noise Reduction:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(options_frame, textvariable=self.noise_reduction, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to process")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Process", command=self.start_processing)
        self.process_button.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Configure row weights
        for i in range(8):
            main_frame.rowconfigure(i, weight=0)
        main_frame.rowconfigure(4, weight=1)  # Options frame can expand
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if file_path:
            self.image_path.set(file_path)
    
    def browse_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.pdf_path.set(file_path)
    
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Output PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)
    
    def start_processing(self):
        # Validate inputs
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image file.")
            return
            
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF file.")
            return
            
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify an output file.")
            return
        
        # Start processing in a separate thread to keep UI responsive
        self.process_button.config(state="disabled")
        self.status_label.config(text="Processing...")
        self.progress.start()
        
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()
    
    def process_files(self):
        try:
            # Get values from UI
            image_path = self.image_path.get()
            pdf_path = self.pdf_path.get()
            output_path = self.output_path.get()
            threshold_str = self.threshold_value.get()
            no_perspective = self.no_perspective.get()
            noise_str = self.noise_reduction.get()
            
            # Convert threshold value
            threshold = None
            if threshold_str:
                try:
                    threshold = int(threshold_str)
                    if not (0 <= threshold <= 255):
                        raise ValueError("Threshold must be between 0 and 255")
                except ValueError as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Invalid threshold value: {e}"))
                    self.root.after(0, self.reset_ui)
                    return
            
            # Convert noise reduction value
            try:
                noise_reduction = int(noise_str)
                if noise_reduction < 0:
                    raise ValueError("Noise reduction must be non-negative")
            except ValueError as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Invalid noise reduction value: {e}"))
                self.root.after(0, self.reset_ui)
                return
            
            # Validate input files
            validate_input_files(image_path, pdf_path)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Define a temporary path for the SVG file
            temp_svg_path = os.path.join(output_dir, "temp.svg") if output_dir else "temp.svg"

            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Loading image..."))
            
            # Load the image
            image = load_image(image_path)
            if image is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            # Correct the perspective (if requested)
            if not no_perspective:
                self.root.after(0, lambda: self.status_label.config(text="Correcting perspective..."))
                corrected_image = correct_perspective(image)
            else:
                self.root.after(0, lambda: self.status_label.config(text="Skipping perspective correction..."))
                corrected_image = image
            
            # Preprocess the image
            self.root.after(0, lambda: self.status_label.config(text="Preprocessing image..."))
            grayscale_image = to_grayscale(corrected_image)
            
            # Apply thresholding (binary or adaptive)
            if threshold is not None:
                self.root.after(0, lambda: self.status_label.config(text=f"Applying binary threshold with value {threshold}..."))
                from preprocessing import apply_binary_threshold
                binary_image = apply_binary_threshold(grayscale_image, threshold)
            else:
                self.root.after(0, lambda: self.status_label.config(text="Applying adaptive threshold..."))
                binary_image = apply_adaptive_threshold(grayscale_image)
            
            # Apply noise reduction
            if noise_reduction > 0:
                self.root.after(0, lambda: self.status_label.config(text=f"Reducing noise with strength {noise_reduction}..."))
                # Ensure noise reduction value is odd
                noise_reduction_val = noise_reduction if noise_reduction % 2 == 1 else noise_reduction + 1
                denoised_image = reduce_noise(binary_image, noise_reduction_val)
            else:
                self.root.after(0, lambda: self.status_label.config(text="Skipping noise reduction..."))
                denoised_image = binary_image
            
            # Find contours
            self.root.after(0, lambda: self.status_label.config(text="Finding contours..."))
            contours = find_contours(denoised_image)
            
            # Convert contours to SVG
            self.root.after(0, lambda: self.status_label.config(text="Converting to SVG..."))
            height, width = corrected_image.shape[:2]
            contours_to_svg(contours, width, height, temp_svg_path)
            
            # Overlay the SVG on the PDF
            self.root.after(0, lambda: self.status_label.config(text="Overlaying SVG on PDF..."))
            overlay_svg_on_pdf(pdf_path, temp_svg_path, output_path)
            
            # Clean up the temporary SVG file
            if os.path.exists(temp_svg_path):
                os.remove(temp_svg_path)
            
            # Success
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Successfully created final PDF at:\n{output_path}"))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {error_msg}"))
        finally:
            self.root.after(0, self.reset_ui)
    
    def reset_ui(self):
        self.process_button.config(state="normal")
        self.status_label.config(text="Ready to process")
        self.progress.stop()

def main():
    root = tk.Tk()
    app = HandNoteToPDFGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()