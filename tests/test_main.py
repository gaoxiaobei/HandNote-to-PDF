# HandNote-to-PDF/tests/test_main.py

import unittest
import os
import sys
import tempfile
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import validate_input_files

class TestMain(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        shutil.rmtree(self.test_dir)
        
    def test_validate_input_files_valid(self):
        """Test validation with valid files."""
        # Create dummy files
        image_path = os.path.join(self.test_dir, "test.png")
        pdf_path = os.path.join(self.test_dir, "test.pdf")
        
        with open(image_path, "wb") as f:
            f.write(b"fake png content")
            
        with open(pdf_path, "wb") as f:
            f.write(b"fake pdf content")
            
        # This should not raise an exception
        validate_input_files(image_path, pdf_path)
        
    def test_validate_input_files_missing_image(self):
        """Test validation with missing image file."""
        pdf_path = os.path.join(self.test_dir, "test.pdf")
        
        with open(pdf_path, "wb") as f:
            f.write(b"fake pdf content")
            
        with self.assertRaises(FileNotFoundError):
            validate_input_files("nonexistent.png", pdf_path)
            
    def test_validate_input_files_missing_pdf(self):
        """Test validation with missing PDF file."""
        image_path = os.path.join(self.test_dir, "test.png")
        
        with open(image_path, "wb") as f:
            f.write(b"fake png content")
            
        with self.assertRaises(FileNotFoundError):
            validate_input_files(image_path, "nonexistent.pdf")
            
    def test_validate_input_files_wrong_image_format(self):
        """Test validation with wrong image format."""
        image_path = os.path.join(self.test_dir, "test.txt")
        pdf_path = os.path.join(self.test_dir, "test.pdf")
        
        with open(image_path, "wb") as f:
            f.write(b"fake text content")
            
        with open(pdf_path, "wb") as f:
            f.write(b"fake pdf content")
            
        with self.assertRaises(ValueError):
            validate_input_files(image_path, pdf_path)
            
    def test_validate_input_files_wrong_pdf_format(self):
        """Test validation with wrong PDF format."""
        image_path = os.path.join(self.test_dir, "test.png")
        pdf_path = os.path.join(self.test_dir, "test.txt")
        
        with open(image_path, "wb") as f:
            f.write(b"fake png content")
            
        with open(pdf_path, "wb") as f:
            f.write(b"fake text content")
            
        with self.assertRaises(ValueError):
            validate_input_files(image_path, pdf_path)

if __name__ == '__main__':
    unittest.main()