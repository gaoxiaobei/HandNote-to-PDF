import cv2
import numpy as np
import sys

def _order_points(pts):
    """Orders the four points of a rectangle in a consistent order."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def load_image(image_path):
    """Loads an image from the specified path."""
    # Handle potential encoding issues with file paths
    try:
        # Try to open the file first to check if it exists and is accessible
        with open(image_path, 'rb') as f:
            pass
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image from {image_path}. Check if the file exists and is a valid image.", file=sys.stderr)
        return image
    except Exception as e:
        print(f"Error accessing file {image_path}: {e}", file=sys.stderr)
        return None

def correct_perspective(image):
    """Finds the corners of a document and corrects the perspective."""
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        screen_cnt = None
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                screen_cnt = approx
                break
        
        if screen_cnt is None:
            print("Warning: Could not detect document corners. Using original image.", file=sys.stderr)
            # If no 4-point contour is found, return the original image
            return image

        pts = _order_points(screen_cnt.reshape(4, 2))
        (tl, tr, br, bl) = pts

        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))

        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))

        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]], dtype="float32")

        m = cv2.getPerspectiveTransform(pts, dst)
        warped = cv2.warpPerspective(image, m, (max_width, max_height))
        return warped
    except Exception as e:
        print(f"Error in perspective correction: {e}", file=sys.stderr)
        return image

def to_grayscale(image):
    """Converts an image to grayscale."""
    try:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(f"Error in grayscale conversion: {e}", file=sys.stderr)
        raise

def apply_binary_threshold(image, threshold_value=128):
    """Applies a binary threshold to the image."""
    try:
        _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)
        return binary_image
    except Exception as e:
        print(f"Error in binary thresholding: {e}", file=sys.stderr)
        raise

def apply_adaptive_threshold(image):
    """Applies an adaptive threshold to the image."""
    try:
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)
    except Exception as e:
        print(f"Error in adaptive thresholding: {e}", file=sys.stderr)
        raise

def reduce_noise(image, kernel_size=5):
    """Reduces noise in the image using a median blur."""
    try:
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.medianBlur(image, kernel_size)
    except Exception as e:
        print(f"Error in noise reduction: {e}", file=sys.stderr)
        raise
