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
    # 1. Immediate visual feedback
    st.toast(f"🌀 Callback triggered for Page {page_num}")
    
    # 2. Safely get the version
    v = st.session_state.get(f"v_{page_num}", 0)
    uploader_key = f"u_{page_num}_v{v}"
    
    # 3. List all keys to the UI so you can see them
    all_keys = [k for k in st.session_state.keys() if k.startswith(f"u_{page_num}")]
    st.write(f"Looking for: `{uploader_key}` | Found keys: `{all_keys}`")
    
    uploaded_file = st.session_state.get(uploader_key)
    
    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            img = ImageOps.exif_transpose(img).convert("RGBA")
            img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            
            st.session_state.pages[page_num]["image"] = img
            st.toast("✅ Image processed!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning(f"No file found for key: {uploader_key}")
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