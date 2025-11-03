import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
import base64

# Set page config
st.set_page_config(
    page_title="BINI ASCII Player Web",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better ASCII display
st.markdown("""
<style>
.ascii-art {
    font-family: 'Courier New', monospace;
    font-size: 8px;
    line-height: 8px;
    white-space: pre;
    background-color: black;
    color: white;
    padding: 10px;
    border-radius: 5px;
    max-height: 600px;
    overflow: auto;
}
.parrot {
    font-family: 'Courier New', monospace;
    white-space: pre;
    color: #00ff00;
}
</style>
""", unsafe_allow_html=True)

class StreamlitASCIIConverter:
    def __init__(self):
        self.chars = "@%#*+=-:. "
        self.color_chars = " ░▒▓█"
    
    def image_to_ascii(self, image, width=100, color_mode=False):
        """Convert image to ASCII art"""
        # Convert to grayscale if not color mode
        if color_mode:
            img_rgb = image.convert('RGB')
            img_gray = image.convert('L')
        else:
            img_gray = image.convert('L')
            img_rgb = None
        
        # Calculate dimensions
        aspect_ratio = img_gray.height / img_gray.width
        height = int(width * aspect_ratio * 0.5)
        
        # Resize
        img_resized = img_gray.resize((width, height))
        if color_mode:
            img_rgb_resized = img_rgb.resize((width, height))
        
        # Convert to arrays
        pixels_gray = np.array(img_resized)
        if color_mode:
            pixels_rgb = np.array(img_rgb_resized)
        
        # Create ASCII art
        ascii_lines = []
        scale = len(self.chars) - 1
        
        for y in range(height):
            line = ""
            for x in range(width):
                brightness = pixels_gray[y, x]
                char = self.chars[min(int(brightness / 255 * scale), scale)]
                
                if color_mode:
                    r, g, b = pixels_rgb[y, x]
                    # Create colored character (simplified for web)
                    line += char
                else:
                    line += char
            
            ascii_lines.append(line)
        
        return '\n'.join(ascii_lines)
    
    def video_frame_to_ascii(self, frame, width=80):
        """Convert video frame to ASCII"""
        # Resize frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        aspect_ratio = frame.shape[0] / frame.shape[1]
        height = int(width * aspect_ratio * 0.5)
        
        frame_resized = cv2.resize(frame_gray, (width, height))
        
        # Convert to ASCII
        ascii_lines = []
        scale = len(self.chars) - 1
        
        for row in frame_resized:
            ascii_row = ''.join(self.chars[min(int(pixel / 255 * scale), scale)] for pixel in row)
            ascii_lines.append(ascii_row)
        
        return '\n'.join(ascii_lines)

def main():
    st.title("🎬 BINI ASCII Player - Web Version")
    st.markdown("Experience ASCII art in your browser!")
    
    # Initialize converter
    converter = StreamlitASCIIConverter()
    
    # Sidebar for options
    st.sidebar.title("Options")
    ascii_width = st.sidebar.slider("ASCII Width", 40, 150, 80)
    color_mode = st.sidebar.checkbox("Color Mode (Experimental)", False)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Image to ASCII", "🎬 Video to ASCII", "🦜 Parrot", "📚 About"])
    
    with tab1:
        st.header("Convert Images to ASCII Art")
        
        uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png', 'bmp'])
        
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)
            
            with col2:
                st.subheader("ASCII Art")
                ascii_art = converter.image_to_ascii(image, width=ascii_width, color_mode=color_mode)
                st.markdown(f'<div class="ascii-art">{ascii_art}</div>', unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="Download ASCII Art",
                    data=ascii_art,
                    file_name="ascii_art.txt",
                    mime="text/plain"
                )
    
    with tab2:
        st.header("Convert Video to ASCII")
        st.info("Note: Video processing is limited in web version. For full video playback, use the local package.")
        
        uploaded_video = st.file_uploader("Choose a video", type=['mp4', 'avi', 'mov'])
        
        if uploaded_video is not None:
            # Save uploaded video to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_video.read())
                video_path = tmp_file.name
            
            # Read video
            cap = cv2.VideoCapture(video_path)
            
            if cap.isOpened():
                # Get video info
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                st.write(f"Video: {total_frames} frames, {fps:.1f} FPS")
                
                # Process first frame as preview
                ret, frame = cap.read()
                if ret:
                    st.subheader("First Frame Preview")
                    ascii_preview = converter.video_frame_to_ascii(frame, width=ascii_width)
                    st.markdown(f'<div class="ascii-art">{ascii_preview}</div>', unsafe_allow_html=True)
                
                cap.release()
            
            # Clean up
            os.unlink(video_path)
    
    with tab3:
        st.header("🦜 Party Parrot")
        
        # Animated parrot frames
        parrot_frames = [
            r"""
   _
  ( \
   \ \
    \ \  
    / /                 
   / / 
  ( (  
   \ \
    ) )
   / / 
  / /  
 ( (   
  \_\  
            """,
            r"""
   _
  ( \
   \ \
    \ \  
    / /                 
   / / 
  ( (  
   \ \
    ) )
   / / 
  / /  
 ( (   
  \_\  
            """
        ]
        
        if st.button("Animate Parrot!"):
            placeholder = st.empty()
            for i in range(10):  # Show 10 cycles
                for frame in parrot_frames:
                    placeholder.markdown(f'<div class="parrot">{frame}</div>', unsafe_allow_html=True)
                    import time
                    time.sleep(0.3)
            
            st.success("🎵 Party parrot finished! 🎵")
        
        # Static parrot display
        st.markdown(f'<div class="parrot">{parrot_frames[0]}</div>', unsafe_allow_html=True)
    
    with tab4:
        st.header("About BINI ASCII Player")
        st.markdown("""
        ### 🎬 Full Features Available Locally
        
        This web version demonstrates basic ASCII conversion. For the full experience with:
        
        - ✅ **Real-time video playback**
        - ✅ **Full color ASCII art**
        - ✅ **Interactive controls**
        - ✅ **Camera support**
        - ✅ **Full screen terminal mode**
        
        Install the local package:
        ```bash
        pip install bini-terminal-ascii-player
        ```
        
        Then use:
        ```bash
        bini play video.mp4
        bini parrot
        bini image photo.jpg
        ```
        
        ### 🛠️ Technical Details
        - Built with Streamlit
        - OpenCV for image processing
        - Pillow for image handling
        - Pure Python ASCII conversion
        """)

if __name__ == "__main__":
    main()