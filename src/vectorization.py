import cv2
import svgwrite

def find_contours(image):
    """Finds contours in a binary image."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def contours_to_svg(contours, width, height, output_file):
    """Converts contours to an SVG file."""
    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(width, height))
    for contour in contours:
        path_data = "M" + " L".join(f"{p[0][0]},{p[0][1]}" for p in contour)
        dwg.add(dwg.path(d=path_data, stroke="black", fill="none"))
    dwg.save()
