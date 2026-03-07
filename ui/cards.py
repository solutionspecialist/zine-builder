import streamlit as st
from PIL import Image, ImageOps

def page_card(page_num):
    # --- 1. SPREAD CHECK ---
    spread_pairs = {2: 3, 4: 5, 6: 7, 8: 1}
    is_covered = False
    for anchor, target in spread_pairs.items():
        if page_num == target and st.session_state.pages.get(anchor, {}).get("is_spread"):
            is_covered = True
            break

    st.markdown(f"### Page {page_num}")
    
    if page_num not in st.session_state.pages:
        st.session_state.pages[page_num] = {
            "image": None, "scale_mode": "fill", "is_spread": False
        }
    
    page = st.session_state.pages[page_num]

    # --- 2. SMART UPLOAD HELPER ---
    def handle_upload():
        uploader_key = f"uploader_{page_num}"
        if st.session_state[uploader_key]:
            img = Image.open(st.session_state[uploader_key])
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGB")
            
            # Resize to a max of 1200px (High quality but efficient)
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            
            st.session_state.pages[page_num]["image"] = img

    # --- 3. UI RENDERING ---
    main_col_left, main_col_right = st.columns([1.5, 1])

    with main_col_left:
        preview_container = st.container(height=250, border=True)
        with preview_container:
            if is_covered:
                st.info("↔️ Part of a spread.")
            elif page["image"]:
                # The preview displays the exact state of the PIL object
                st.image(page["image"], width="stretch")
            else:
                st.info("Empty Slot")
        
        st.file_uploader(
            f"Upload {page_num}", 
            type=["jpg", "jpeg", "png"], 
            key=f"uploader_{page_num}", 
            label_visibility="collapsed",
            disabled=is_covered,
            on_change=handle_upload
        )

    with main_col_right:
        if not is_covered and page["image"]:
            # --- PHYSICAL ROTATION ---
            if st.button(f"Rotate ↻", key=f"rot_{page_num}", width="stretch"):
                # Rotate the actual pixels 90 degrees CCW
                page["image"] = page["image"].rotate(-90, expand=True)
                st.rerun()
            
            if st.button("🗑️ Clear", key=f"del_{page_num}", width="stretch"):
                page["image"] = None
                st.session_state[f"uploader_{page_num}"] = None
                st.rerun()

            page["scale_mode"] = st.radio("Fit", ["fit", "fill"], 
                                         index=1 if page["scale_mode"] == "fill" else 0,
                                         key=f"scale_{page_num}", horizontal=True)

            if page_num in [2, 4, 6, 8]:
                target = 1 if page_num == 8 else page_num + 1
                page["is_spread"] = st.toggle(f"Spread to {target}", value=page["is_spread"], key=f"spread_{page_num}")
        elif is_covered:
            st.caption("Locked by anchor.")
        else:
            st.caption("Upload an image.")