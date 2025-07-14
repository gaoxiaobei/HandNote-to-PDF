import cv2
import numpy as np

def load_image(image_path):
    """Loads an image from the specified path."""
    return cv2.imread(image_path)

def to_grayscale(image):
    """Converts an image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_binary_threshold(image, threshold_value=128):
    """Applies a binary threshold to the image."""
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)
    return binary_image

def reduce_noise(image):
    """Reduces noise in the image using a median blur."""
    return cv2.medianBlur(image, 5)
