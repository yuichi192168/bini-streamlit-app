import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import base64
import io
import time

# Set page config
st.set_page_config(
    page_title="BINI ASCII Player Web",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS with #63CBD6 color theme
st.markdown("""
<style>
:root {
    --primary-color: #63CBD6;
    --primary-dark: #4BA8B0;
    --primary-light: #8BD9E0;
}

.ascii-art {
    font-family: 'Courier New', monospace;
    font-size: 8px;
    line-height: 8px;
    white-space: pre;
    background-color: #0A0A0A;
    color: #63CBD6;
    padding: 15px;
    border-radius: 8px;
    max-height: 600px;
    overflow: auto;
    border: 1px solid #63CBD6;
    box-shadow: 0 4px 12px rgba(99, 203, 214, 0.2);
}

.primary-button {
    background-color: #63CBD6 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-weight: 600 !important;
}

.primary-button:hover {
    background-color: #4BA8B0 !important;
    transform: translateY(-1px);
    transition: all 0.2s ease;
}

.info-box {
    background: linear-gradient(135deg, rgba(99, 203, 214, 0.1), rgba(99, 203, 214, 0.05));
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #63CBD6;
    border-top: 1px solid rgba(99, 203, 214, 0.2);
}

.feature-card {
    background: rgba(99, 203, 214, 0.05);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(99, 203, 214, 0.2);
    margin: 10px 0;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(99, 203, 214, 0.1);
    border-radius: 4px 4px 0px 0px;
    padding: 8px 16px;
    border: 1px solid rgba(99, 203, 214, 0.2);
}

.stTabs [aria-selected="true"] {
    background-color: #63CBD6 !important;
    color: white !important;
}

h1, h2, h3 {
    color: #63CBD6 !important;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, rgba(99, 203, 214, 0.05) 0%, transparent 100%);
}

.download-btn {
    background: linear-gradient(135deg, #63CBD6, #4BA8B0) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
}

.download-btn:hover {
    background: linear-gradient(135deg, #4BA8B0, #63CBD6) !important;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

class StreamlitASCIIConverter:
    def __init__(self):
        self.chars = "@%#*+=-:. "
        self.color_chars = " ░▒▓█"
    
    def enhance_image(self, image):
        """Enhance image for better ASCII conversion"""
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        return image
    
    def image_to_ascii(self, image, width=100, enhanced=True):
        """Convert image to ASCII art without OpenCV"""
        # Enhance image if requested
        if enhanced:
            image = self.enhance_image(image)
        
        # Convert to grayscale
        img_gray = image.convert('L')
        
        # Calculate dimensions
        aspect_ratio = img_gray.height / img_gray.width
        height = int(width * aspect_ratio * 0.5)
        
        # Resize
        img_resized = img_gray.resize((width, height), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        pixels = np.array(img_resized)
        
        # Create ASCII art
        ascii_lines = []
        scale = len(self.chars) - 1
        
        for row in pixels:
            ascii_row = ''.join(self.chars[min(int(pixel / 255 * scale), scale)] for pixel in row)
            ascii_lines.append(ascii_row)
        
        return '\n'.join(ascii_lines)
    
    def create_color_ascii(self, image, width=80):
        """Create color ASCII art (simulated)"""
        img_rgb = image.convert('RGB')
        aspect_ratio = img_rgb.height / img_rgb.width
        height = int(width * aspect_ratio * 0.5)
        
        img_resized = img_rgb.resize((width, height), Image.Resampling.LANCZOS)
        pixels = np.array(img_resized)
        
        ascii_lines = []
        scale = len(self.chars) - 1
        
        for row in pixels:
            ascii_row = ""
            for pixel in row:
                r, g, b = pixel
                brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                char = self.chars[min(int(brightness / 255 * scale), scale)]
                ascii_row += char
            ascii_lines.append(ascii_row)
        
        return '\n'.join(ascii_lines)

def main():
    st.title("🎬 BINI ASCII Player - Web Version")
    st.markdown("### Transform your images into beautiful ASCII art with our cyan-themed converter! ✨")
    
    # Initialize converter
    converter = StreamlitASCIIConverter()
    
    # Sidebar for options
    st.sidebar.title("⚙️ Conversion Settings")
    ascii_width = st.sidebar.slider("ASCII Width", 40, 120, 80)
    enhance_image = st.sidebar.checkbox("Enhance Image Quality", True)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎨 Image Converter", "🌟 Live Demos", "📚 About & Installation"])
    
    with tab1:
        st.header("🎨 Image to ASCII Converter")
        st.markdown("Upload any image and watch it transform into stunning cyan-colored ASCII art!")
        
        uploaded_file = st.file_uploader(
            "📁 Choose an image file", 
            type=['jpg', 'jpeg', 'png', 'bmp', 'gif'],
            help="Supported formats: JPG, PNG, BMP, GIF"
        )
        
        if uploaded_file is not None:
            try:
                # Display original image
                image = Image.open(uploaded_file)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📷 Original Image")
                    st.image(image, use_column_width=True, caption="Your original image")
                    
                    # Image info
                    st.markdown("""
                    <div class="feature-card">
                    <strong>📊 Image Information</strong><br>
                    • Dimensions: {} x {}<br>
                    • Format: {}<br>
                    • Mode: {}
                    </div>
                    """.format(image.size[0], image.size[1], image.format, image.mode), unsafe_allow_html=True)
                
                with col2:
                    st.subheader("🔤 ASCII Art Preview")
                    
                    # Convert to ASCII
                    with st.spinner('🔄 Converting to ASCII art...'):
                        ascii_art = converter.image_to_ascii(
                            image, 
                            width=ascii_width, 
                            enhanced=enhance_image
                        )
                    
                    # Display ASCII art
                    st.markdown(f'<div class="ascii-art">{ascii_art}</div>', unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="💾 Download ASCII Art",
                        data=ascii_art,
                        file_name="ascii_art.txt",
                        mime="text/plain",
                        help="Download the ASCII art as a text file",
                        key="download_ascii"
                    )
                    
                    # ASCII stats
                    lines = ascii_art.split('\n')
                    st.markdown(f"""
                    <div class="feature-card">
                    <strong>📐 ASCII Art Statistics</strong><br>
                    • Dimensions: {len(lines[0])} × {len(lines)} characters<br>
                    • Total characters: {len(ascii_art.replace(chr(10), ''))}<br>
                    • Color theme: #63CBD6 (Cyan)
                    </div>
                    """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
        else:
            st.info("👆 Upload an image above to get started!")
    
    with tab2:
        st.header("🌟 Live ASCII Demos")
        st.markdown("Try our built-in demo images to see the ASCII conversion in action!")
        
        # Sample images
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎨 Gradient Demo", use_container_width=True):
                gradient_img = create_gradient_image()
                ascii_art = converter.image_to_ascii(gradient_img, width=ascii_width)
                st.markdown(f'<div class="ascii-art">{ascii_art}</div>', unsafe_allow_html=True)
                st.success("✨ Smooth gradient converted to ASCII!")
        
        with col2:
            if st.button("🔷 Shapes Demo", use_container_width=True):
                shapes_img = create_shapes_image()
                ascii_art = converter.image_to_ascii(shapes_img, width=ascii_width)
                st.markdown(f'<div class="ascii-art">{ascii_art}</div>', unsafe_allow_html=True)
                st.success("🎯 Geometric shapes converted to ASCII!")
        
        with col3:
            if st.button("🌀 Pattern Demo", use_container_width=True):
                pattern_img = create_pattern_image()
                ascii_art = converter.image_to_ascii(pattern_img, width=ascii_width)
                st.markdown(f'<div class="ascii-art">{ascii_art}</div>', unsafe_allow_html=True)
                st.success("🌊 Complex pattern converted to ASCII!")
        
        # Demo explanation
        st.markdown("""
        <div class="info-box">
        <h4>🎯 About the Demos</h4>
        <p>These demo images showcase how different visual elements convert to ASCII art:</p>
        <ul>
        <li><strong>Gradient</strong>: Shows smooth transitions from dark to light</li>
        <li><strong>Shapes</strong>: Demonstrates how geometric forms translate to ASCII</li>
        <li><strong>Pattern</strong>: Exhibits complex texture conversion</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.header("📚 About BINI ASCII Player")
        
        st.markdown("""
        <div class="info-box">
        <h3>🎬 Full Features Available Locally</h3>
        <p>This web version demonstrates basic ASCII conversion with our beautiful cyan theme. For the complete experience with real-time video playback and advanced features, install the local package!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Installation instructions
        st.subheader("🚀 Quick Installation")
        st.code("""
# Install the full package
pip install bini-terminal-ascii-player

# Use all features
bini play video.mp4      # Play videos as ASCII
bini image photo.jpg     # Display images as ASCII  
bini list                # List media files
        """, language="bash")
        
        # Feature comparison
        st.subheader("📊 Feature Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
            <h4>🌐 Web Version</h4>
            ✅ Image to ASCII conversion  <br>
            ✅ Live preview  <br>
            ✅ Download ASCII art  <br>
            ✅ Mobile friendly  <br>
            ✅ Beautiful cyan theme  <br>
            ❌ Real-time video playback  <br>
            ❌ Camera support  <br>
            ❌ Terminal controls
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
            <h4>💻 Local Package</h4>
            ✅ Image to ASCII conversion  <br>
            ✅ Real-time video playback  <br>
            ✅ Full color ASCII art  <br>
            ✅ Camera support  <br>
            ✅ Interactive controls  <br>
            ✅ Full screen terminal  <br>
            ✅ Webcam integration  <br>
            ✅ Advanced features
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Technical details
        st.subheader("🔧 Technical Details")
        st.markdown("""
        <div class="feature-card">
        <strong>Web Framework</strong>: Streamlit<br>
        <strong>Image Processing</strong>: Pillow (PIL)<br>
        <strong>ASCII Algorithm</strong>: Custom brightness mapping<br>
        <strong>Color Theme</strong>: #63CBD6 (Cyan)<br>
        <strong>Deployment</strong>: Streamlit Cloud
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎨 About the Color Theme
        The beautiful cyan color (#63CBD6) used throughout this app represents:
        - **Creativity** and **innovation** in digital art
        - **Clarity** and **precision** in ASCII conversion
        - **Modern** and **clean** aesthetic design
        - **Calm** and **focused** user experience
        """)

def create_gradient_image():
    """Create a gradient image for demo"""
    width, height = 200, 100
    gradient = Image.new('L', (width, height))
    pixels = []
    
    for y in range(height):
        for x in range(width):
            brightness = int(255 * (x / width))
            pixels.append(brightness)
    
    gradient.putdata(pixels)
    return gradient

def create_shapes_image():
    """Create an image with shapes for demo"""
    img = Image.new('L', (200, 100), color=128)
    
    # Draw some simple shapes
    for y in range(100):
        for x in range(200):
            # Circle
            if (x-100)**2 + (y-50)**2 < 400:
                img.putpixel((x, y), 255)
            # Rectangle
            if 50 <= x <= 150 and 20 <= y <= 80:
                img.putpixel((x, y), 50)
    
    return img

def create_pattern_image():
    """Create a pattern image for demo"""
    img = Image.new('L', (200, 100))
    
    for y in range(100):
        for x in range(200):
            brightness = (x * y) % 256
            img.putpixel((x, y), brightness)
    
    return img

if __name__ == "__main__":
    main()