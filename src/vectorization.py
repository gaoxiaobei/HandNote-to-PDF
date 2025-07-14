import cv2
import svgwrite
import numpy as np

def _simplify_contour(contour, epsilon_factor=0.002):
    """Simplifies a contour using the Ramer-Douglas-Peucker algorithm."""
    perimeter = cv2.arcLength(contour, True)
    epsilon = epsilon_factor * perimeter
    return cv2.approxPolyDP(contour, epsilon, True)

def _fit_curve(points):
    """Fits a Bézier curve to a set of points and returns the SVG path data."""
    if len(points) < 2:
        return ""

    path_data = f"M{points[0][0][0]},{points[0][0][1]}"
    for i in range(len(points) - 1):
        p1 = points[i][0]
        p2 = points[i+1][0]
        # For simplicity, we'll use quadratic Bézier curves.
        # The control point is the midpoint between the two points.
        cx = (p1[0] + p2[0]) / 2
        cy = (p1[1] + p2[1]) / 2
        path_data += f" Q{cx},{cy} {p2[0]},{p2[1]}"
    return path_data

def find_contours(image):
    """Finds contours in a binary image."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def contours_to_svg(contours, width, height, output_file):
    """Converts contours to an SVG file using curve fitting."""
    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(width, height))
    for contour in contours:
        simplified_contour = _simplify_contour(contour)
        path_data = _fit_curve(simplified_contour)
        if path_data:
            dwg.add(dwg.path(d=path_data, stroke="black", fill="none", stroke_width=2))
    dwg.save()
