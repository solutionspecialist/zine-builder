import streamlit as st

def page_card(page_num):
    # --- 1. SPREAD CHECK ---
    # Determine if this page is currently covered by a spread from an anchor
    spread_pairs = {2: 3, 4: 5, 6: 7, 8: 1}
    is_covered = False
    for anchor, target in spread_pairs.items():
        if page_num == target and st.session_state.pages.get(anchor, {}).get("is_spread"):
            is_covered = True
            break

    st.markdown(f"### Page {page_num}")
    
    # Initialize state with 'fill' as the default
    if page_num not in st.session_state.pages:
        st.session_state.pages[page_num] = {
            "image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False
        }
    
    page = st.session_state.pages[page_num]

    # --- 2. CSS INJECTION ---
    # This targets the specific data-testids you found to hide the file list & x
    st.markdown("""
        <style>
            div[data-testid="stFileUploaderFile"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 3. UI RENDERING ---
    main_col_left, main_col_right = st.columns([1.5, 1])

    with main_col_left:
        preview_container = st.container(height=250, border=True)
        
        with preview_container:
            if is_covered:
                st.info("↔️ This slot is part of a 2-page spread.")
            elif page["image"]:
                st.image(page["image"], width="stretch")
            else:
                st.info("Empty Slot")
        
        # Disable uploader if the page is covered by a spread
        uploaded_file = st.file_uploader(
            f"Upload Image {page_num}", 
            type=["jpg", "jpeg", "png"], 
            key=f"uploader_{page_num}", 
            label_visibility="collapsed",
            disabled=is_covered
        )
        if uploaded_file and not is_covered:
            page["image"] = uploaded_file

    with main_col_right:
        st.markdown("**Page Options**")
        
        # Disable all options if covered
        if is_covered:
            st.caption("Locked: Controlling via spread anchor.")
        elif page["image"]:
            if st.button(f"Rotate ↻", key=f"rot_{page_num}", width="stretch"):
                page["rotation"] = (page["rotation"] + 90) % 360
            
            if st.button("🗑️ Clear", key=f"del_{page_num}", width="stretch"):
                page["image"] = None
                st.rerun()

            st.divider()

            page["scale_mode"] = st.radio(
                "Fitment", ["fit", "fill"], 
                index=1 if page["scale_mode"] == "fill" else 0,
                key=f"scale_{page_num}",
                horizontal=True
            )

            anchor_pages = [2, 4, 6, 8]
            if page_num in anchor_pages:
                target = 1 if page_num == 8 else page_num + 1
                page["is_spread"] = st.toggle(
                    f"🎨 Spread to Page {target}", 
                    value=page["is_spread"], 
                    key=f"spread_{page_num}"
                )
        else:
            st.caption("Upload an image to see options.")