import streamlit as st
from model_helper import predict
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="Fruit Freshness Checker", 
    page_icon="🍎", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional styling
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    /* Title styling */
    .title-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 2rem;
    }
    
    .main-title {
        color: #2e7d32;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .subtitle {
        color: #66bb6a;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Upload section */
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* File uploader */
    .stFileUploader {
        background: #f1f8f4;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Result boxes */
    .result-fresh {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #43a047;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-top: 1.5rem;
    }
    
    .result-stale {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #e53935;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-top: 1.5rem;
    }
    
    .result-title-fresh {
        color: #1b5e20;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-title-stale {
        color: #b71c1c;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-text {
        color: #424242;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Image container */
    .image-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin: 1.5rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
    <div class="title-container">
        <div class="main-title">🍎 Fruit Freshness Checker</div>
        <div class="subtitle">AI-Powered Freshness Detection System</div>
    </div>
""", unsafe_allow_html=True)

# Instructions
st.markdown("### 📸 Upload Your Fruit Image")
st.markdown("Support for: Banana, Lemon, Lulo, Mango, Orange, Strawberry, Tamarillo, Tomato")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=["jpg", "png", "jpeg"],
    help="Upload a clear image of the fruit"
)

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Save temporary file
    image_path = "temp_fruit.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Check freshness button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔍 Analyze Freshness"):
        with st.spinner("🤖 AI is analyzing your fruit..."):
            prediction, fruit_type, freshness = predict(image_path)
            
            # Display result with appropriate styling
            if freshness == "Fresh":
                st.markdown(f"""
                    <div class="result-fresh">
                        <div class="result-title-fresh">✅ Fresh {fruit_type}!</div>
                        <div class="result-text">
                            <strong>Classification:</strong> {prediction}<br>
                            <strong>Status:</strong> This {fruit_type} looks fresh and ready to eat. 
                            It appears to be in excellent condition with good quality.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-stale">
                        <div class="result-title-stale">⚠️ Stale {fruit_type}</div>
                        <div class="result-text">
                            <strong>Classification:</strong> {prediction}<br>
                            <strong>Status:</strong> This {fruit_type} appears to be past its prime. 
                            Consider checking for signs of spoilage before consumption.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)

else:
    # Empty state
    st.info("👆 Please upload a fruit image to get started")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #757575; font-size: 0.9rem;'>
        Powered by ResNet50 Deep Learning Model
    </div>
""", unsafe_allow_html=True)