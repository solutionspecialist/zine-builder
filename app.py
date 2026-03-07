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
    st.session_state.pages = {
        i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False} 
        for i in range(1, 9)
    }

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
        st.session_state.pages = {
            i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False} 
            for i in range(1, 9)
        }
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
    layout_cols = {5:0, 4:1, 3:2, 2:3, 6:0, 7:1, 8:2, 1:3}
    
    pages_to_process = [n for n, d in st.session_state.pages.items() if d["image"]]
    total_steps = len(pages_to_process)

    if total_steps == 0:
        st.error("Please upload images first!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Points conversion for Letter Landscape
        slot_w = (11 * 72) / 4 
        slot_h = (8.5 * 72) / 2

        for i, num in enumerate(pages_to_process):
            data = st.session_state.pages[num]
            status_text.text(f"Processing Page {num}...")
            
            is_spread = data.get("is_spread", False)
            col = layout_cols[num]
            
            usable_h = slot_h - (margin * 2)
            
            if is_spread:
                usable_w = (slot_w * 2) - (margin * 2)
            else:
                if col in [0, 3]:
                    usable_w = slot_w - margin - gutter
                else:
                    usable_w = slot_w - (gutter * 2)

            # Called using the simple 'process_image' name
            processed_img, w, h = process_image(
                data["image"], 
                data["scale_mode"], 
                usable_w, 
                usable_h
            )
            
            ready_pages[num] = {
                "image": processed_img,
                "display_size": (w, h),
                "is_spread": is_spread
            }
            
            progress_bar.progress((i + 1) / total_steps)

        status_text.text("Finalizing PDF layout...")
        pdf_bytes = create_zine_pdf(ready_pages, show_guides, project_title, margin, gutter)
        
        progress_bar.empty()
        status_text.empty()
        st.success("Zine Ready!")
        
        clean_name = project_title.replace(" ", "_") if project_title else "My_Zine"
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name=f"{clean_name}.pdf",
            mime="application/pdf"
        )