# HandNote-to-PDF/tests/test_preprocessing.py

import unittest
import os
import sys
import numpy as np
import cv2
import tempfile

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessing import load_image, to_grayscale, apply_adaptive_threshold, reduce_noise

class TestPreprocessing(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a simple test image (white background with black square)
        self.test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        # Add a black square
        self.test_image[30:70, 30:70] = [0, 0, 0]
        
        # Save to temporary file
        self.temp_dir = tempfile.mkdtemp()
        self.image_path = os.path.join(self.temp_dir, "test_image.png")
        cv2.imwrite(self.image_path, self.test_image)
        
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_load_image(self):
        """Test loading an image."""
        image = load_image(self.image_path)
        self.assertIsNotNone(image)
        self.assertEqual(image.shape, (100, 100, 3))
        
    def test_load_image_nonexistent(self):
        """Test loading a nonexistent image."""
        image = load_image("nonexistent.png")
        self.assertIsNone(image)
        
    def test_to_grayscale(self):
        """Test converting image to grayscale."""
        gray_image = to_grayscale(self.test_image)
        self.assertEqual(len(gray_image.shape), 2)  # Should be 2D for grayscale
        self.assertEqual(gray_image.shape[0], 100)
        self.assertEqual(gray_image.shape[1], 100)
        
    def test_apply_adaptive_threshold(self):
        """Test applying adaptive threshold."""
        gray_image = to_grayscale(self.test_image)
        binary_image = apply_adaptive_threshold(gray_image)
        self.assertEqual(len(binary_image.shape), 2)  # Should be 2D
        self.assertEqual(binary_image.shape[0], 100)
        self.assertEqual(binary_image.shape[1], 100)
        # All pixels should be either 0 or 255
        unique_vals = np.unique(binary_image)
        for val in unique_vals:
            self.assertIn(val, [0, 255])
            
    def test_reduce_noise(self):
        """Test reducing noise."""
        gray_image = to_grayscale(self.test_image)
        binary_image = apply_adaptive_threshold(gray_image)
        denoised_image = reduce_noise(binary_image)
        self.assertEqual(len(denoised_image.shape), 2)  # Should be 2D
        self.assertEqual(denoised_image.shape[0], 100)
        self.assertEqual(denoised_image.shape[1], 100)

if __name__ == '__main__':
    unittest.main()