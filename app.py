import streamlit as st
from engine.processor import process_image
from engine.generator import create_zine_pdf
from ui.cards import page_card
from ui.styles import apply_custom_css

# 1. Page Configuration
st.set_page_config(page_title="Garford Zine Builder", layout="wide", page_icon="🎨")
apply_custom_css()

# 2. Initialize Session State
if "pages" not in st.session_state:
    st.session_state.pages = {i: {"image": None, "rotation": 0, "scale_mode": "fit", "is_spread": False} for i in range(1, 9)}

# 3. Sidebar / Settings
with st.sidebar:
    st.title("⚙️ Station Settings")
    project_title = st.text_input("Zine Title", value="Garford Fest 2026")
    
    st.divider()
    st.markdown("### Layout Tuning")
    margin = st.slider("Outer Margin (px)", 0, 50, 20)
    gutter = st.slider("Inner Gutter (px)", 0, 30, 10)
    
    show_guides = st.toggle("Show Cut/Fold Guides", value=True)
    
    st.divider()
    if st.button("🔥 Reset All Slots", type="primary", width="stretch"):
        st.session_state.pages = {i: {"image": None, "rotation": 0, "scale_mode": "fit", "is_spread": False} for i in range(1, 9)}
        st.rerun()

st.title("🎨 Garford Zine Builder")
st.caption("Developed for the Garford Arts Fest | August 8, 2026")

# 4. Main UI Grid
for row_idx in range(1, 9, 2):
    row_cols = st.columns(2)
    with row_cols[0]:
        page_card(row_idx)
    with row_cols[1]:
        page_card(row_idx + 1)

st.divider()

# 5. PDF Generation Trigger
if st.button("🚀 Generate Zine PDF", width="stretch", type="primary"):
    ready_pages = {}
    
    # Map page numbers to their horizontal column (0-3)
    layout_cols = {5:0, 4:1, 3:2, 2:3, 6:0, 7:1, 8:2, 1:3}
    
    with st.spinner("Assembling your zine..."):
        slot_w = (11 * 72) / 4 
        slot_h = (8.5 * 72) / 2

        for num, data in st.session_state.pages.items():
            if data["image"]:
                is_spread = data["is_spread"]
                col = layout_cols[num]
                
                usable_h = slot_h - (margin * 2)
                
                if is_spread:
                    # Spreads touch the left and right paper edges
                    usable_w = (slot_w * 2) - (margin * 2)
                else:
                    # Outer columns (0,3) have one margin and one gutter
                    # Inner columns (1,2) have two gutters (no margin)
                    if col in [0, 3]:
                        usable_w = slot_w - margin - gutter
                    else:
                        usable_w = slot_w - (gutter * 2)

                processed_img, w, h = process_image(
                    data["image"], 
                    data["rotation"], 
                    data["scale_mode"], 
                    usable_w, 
                    usable_h
                )
                
                ready_pages[num] = {
                    "image": processed_img,
                    "display_size": (w, h),
                    "is_spread": is_spread,
                    "col": col
                }
        
        if ready_pages:
            pdf_bytes = create_zine_pdf(ready_pages, show_guides, project_title, margin, gutter)
            st.success("Zine Ready!")
            clean_name = project_title.replace(" ", "_") if project_title else "My_Zine"
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{clean_name}.pdf",
                width="stretch",
                mime="application/pdf"
            )
        else:
            st.error("Please upload images first!")