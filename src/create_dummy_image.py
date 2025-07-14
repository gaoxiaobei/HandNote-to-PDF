import numpy as np
import cv2

def create_dummy_image(file_path, width=800, height=600):
    """Creates a dummy image with some text and saves it."""
    # Create a white background
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Add some black text to simulate handwriting
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, 'This is a test note.', (50, 100), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, 'Handwritten notes on a PDF.', (50, 200), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, 'The quick brown fox jumps over the lazy dog.', (50, 300), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Save the image
    cv2.imwrite(file_path, image)

if __name__ == '__main__':
    create_dummy_image('data/dummy_note.png')
