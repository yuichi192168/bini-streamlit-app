import cv2
import numpy as np
from PIL import Image

class AdvancedASCIIConverter:
    def __init__(self):
        self.chars = "@%#*+=-:. "
        self.color_chars = " ░▒▓█"
    
    def enhance_contrast(self, image):
        """Enhance image contrast for better ASCII conversion"""
        img_array = np.array(image)
        # Simple contrast enhancement
        img_enhanced = cv2.convertScaleAbs(img_array, alpha=1.5, beta=0)
        return Image.fromarray(img_enhanced)
    
    def process_video_frame(self, frame, width=80):
        """Process a single video frame for ASCII conversion"""
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Calculate dimensions
        aspect_ratio = frame.shape[0] / frame.shape[1]
        height = int(width * aspect_ratio * 0.5)
        
        # Resize
        frame_resized = cv2.resize(frame_rgb, (width, height))
        frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)
        
        # Convert to ASCII
        ascii_lines = []
        scale = len(self.chars) - 1
        
        for row in frame_gray:
            ascii_row = ''.join(self.chars[min(int(pixel / 255 * scale), scale)] for pixel in row)
            ascii_lines.append(ascii_row)
        
        return '\n'.join(ascii_lines)