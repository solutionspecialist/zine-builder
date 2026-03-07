import streamlit as st
from PIL import Image, ImageOps
import base64
from io import BytesIO

def image_to_base64(img):
    """Converts PIL image to base64 for browser-safe preview."""
    buffered = BytesIO()
    # Save as PNG to preserve transparency/quality in the UI preview
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def handle_upload(page_num):
    print(f"DEBUG: Looking for key {uploader_key}...")
    print(f"DEBUG: Keys currently in session_state: {list(st.session_state.keys())}")
    """Processes image uploads: handles orientation, color mode, and sizing."""
    v = st.session_state[f"v_{page_num}"]
    uploader_key = f"u_{page_num}_v{v}"
    uploaded_file = st.session_state.get(uploader_key)
    
    # Increase the limit to handle professional scans (default is ~89 megapixels)
    Image.MAX_IMAGE_PIXELS = None 
    
    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            img = ImageOps.exif_transpose(img)
            
            # Convert to RGBA for consistency
            img = img.convert("RGBA")
            
            # Use a faster Resampling for the UI thumbnail
            img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            
            st.session_state.pages[page_num]["image"] = img
            
            # CRITICAL: Trigger a rerun so the UI actually shows the change
            st.rerun() 
            
        except Exception as e:
            st.error(f"Critical Error on Page {page_num}: {e}")
            # Log to terminal for a better paper trail
            print(f"FAILED UPLOAD: Page {page_num} | {e}")
    else:
        # If this fires, it means the file was too big or rejected by the server
        print(f"DEBUG: No file found in {uploader_key}. Check maxUploadSize.")

def toggle_spread(page_num):
    """Switches between single page and 2-page spread mode."""
    st.session_state.pages[page_num]["is_spread"] = not st.session_state.pages[page_num]["is_spread"]

def page_card(page_num):
    """Renders the UI card for an individual zine page."""
    if f"v_{page_num}" not in st.session_state:
        st.session_state[f"v_{page_num}"] = 0
    
    page_data = st.session_state.pages[page_num]
    
    # Check if this page is 'covered' by a spread from a previous page
    is_covered = False
    if page_num == 8:
        if st.session_state.pages[1].get("is_spread"): is_covered = True
    elif page_num in [3, 5, 7]:
        if st.session_state.pages[page_num-1].get("is_spread"): is_covered = True

    st.markdown(f"### Page {page_num}")

    with st.container(border=True):
        if is_covered:
            source = 1 if page_num == 8 else page_num - 1
            st.info(f"🔗 Linked to Page {source}")
            st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; font-size: 3rem; opacity: 0.1;'>🔗</div>", unsafe_allow_html=True)
        
        elif page_data["image"]:
            img_b64 = image_to_base64(page_data['image'])
            st.markdown(f"""
                <div style="height: 300px; width: 100%; display: flex; justify-content: center; align-items: center; background-color: #1a1c24; overflow: hidden; border-radius: 8px; margin-bottom: 12px; border: 1px solid #333;">
                    <img src="data:image/png;base64,{img_b64}" style="max-height: 100%; max-width: 100%; object-fit: contain;">
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Rotate", key=f"rot_{page_num}", use_container_width=True):
                    img = page_data["image"].rotate(-90, expand=True)
                    st.session_state.pages[page_num]["image"] = img
                    st.rerun()
                
                mode = "fill" if page_data["scale_mode"] == "fit" else "fit"
                btn_label = "✂️ Use Fill" if mode == "fill" else "🖼️ Use Fit"
                if st.button(btn_label, key=f"mode_{page_num}", use_container_width=True):
                    st.session_state.pages[page_num]["scale_mode"] = mode
                    st.rerun()

            with col2:
                if st.button("🗑️ Clear", key=f"clr_{page_num}", use_container_width=True):
                    st.session_state.pages[page_num]["image"] = None
                    st.session_state.pages[page_num]["is_spread"] = False
                    st.session_state[f"v_{page_num}"] += 1
                    st.rerun()
                
                if page_num in [1, 2, 4, 6]:
                    target = 8 if page_num == 1 else page_num + 1
                    label = "🎨 Wraparound" if page_num == 1 else f"🔗 Link P{target}"
                    st.checkbox(
                        label, 
                        key=f"chk_spread_{page_num}",
                        value=page_data.get("is_spread", False),
                        on_change=toggle_spread,
                        args=(page_num,)
                    )
        else:
            st.markdown("""
                <div style='height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; 
                background-color: #0e1117; border: 1px dashed #444; border-radius: 8px; color: #666;'>
                <span style='font-size: 2rem; margin-bottom: 10px;'>📸</span>
                <span>Select Page Image</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.file_uploader(
                "Upload", type=["jpg", "jpeg", "png", "webp"], 
                key=f"u_{page_num}_v{st.session_state[f'v_{page_num}']}",
                on_change=handle_upload,
                args=(page_num,),
                label_visibility="collapsed"
            )