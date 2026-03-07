import streamlit as st
from PIL import Image, ImageOps
import base64
from io import BytesIO

def image_to_base64(img):
    buffered = BytesIO()
    # If the image is in RGBA (transparency), we save as PNG to preserve it for the preview
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def handle_upload(page_num):
    """Callback for handling image uploads and EXIF orientation."""
    v = st.session_state[f"v_{page_num}"]
    uploader_key = f"u_{page_num}_v{v}"
    uploaded_file = st.session_state.get(uploader_key)
    
    if uploaded_file:
        try:
            st.toast(f"📡 Received {uploaded_file.name}...") # DEBUG
            
            # 1. Open the file
            img = Image.open(uploaded_file)
            
            # 2. Fix Orientation
            img = ImageOps.exif_transpose(img)
            
            # 3. CONVERT TO RGBA FIRST (Safest for PNGs)
            # Some PNGs use "P" (palette) mode which RGB conversion can mangle.
            # RGBA preserves transparency for the UI preview.
            img = img.convert("RGBA")
            
            # 4. Resize for the UI (The likely crash point)
            # We'll use a slightly larger limit but switch to BILINEAR if LANCZOS is failing
            st.toast(f"📐 Processing dimensions...") # DEBUG
            img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            
            # 5. Commit to State
            st.session_state.pages[page_num]["image"] = img
            st.toast(f"✅ Page {page_num} Loaded!") # SUCCESS
            
        except Exception as e:
            st.error(f"🚨 Upload error on Page {page_num}: {e}")
            # Log more details to the streamlit cloud log if available
            print(f"DEBUG ERROR: {e}") 

def toggle_spread(page_num):
    st.session_state.pages[page_num]["is_spread"] = not st.session_state.pages[page_num]["is_spread"]

def page_card(page_num):
    if f"v_{page_num}" not in st.session_state:
        st.session_state[f"v_{page_num}"] = 0
    
    page_data = st.session_state.pages[page_num]
    
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
                    # We use expand=True to ensure the dimensions swap correctly (W <-> H)
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