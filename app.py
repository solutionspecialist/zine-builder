import streamlit as st
from engine.processor import process_image
from engine.generator import create_zine_pdf
from ui.cards import page_card
from ui.styles import apply_custom_css

# Initial Configuration
st.set_page_config(page_title="Garford Zine Builder", layout="centered")
apply_custom_css()

# Session State for Zine Data
if "pages" not in st.session_state:
    st.session_state.pages = {
        i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False} 
        for i in range(1, 9)
    }

# --- SIDEBAR: Settings & Calibration ---
with st.sidebar:
    st.markdown("### 🛠️ Station Settings")
    project_title = st.text_input("Zine Title", value="Garford Fest 2026")
    
    st.divider()
    st.markdown("### 📐 Layout Tuning")
    margin = st.slider("Outer Margin (px)", 0, 50, 0)
    gutter = st.slider("Inner Gutter (px)", 0, 50, 0)
    show_guides = st.toggle("Show Fold Guides", value=True)
    
    st.divider()
    if st.button("🗑️ Reset All Slots", type="secondary", use_container_width=True):
        st.session_state.pages = {
            i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False} 
            for i in range(1, 9)
        }
        st.rerun()

# --- MAIN UI ---
header_col, help_col = st.columns([4, 1])
with header_col:
    st.title("Garford Zine Builder")
    st.caption("Lorain County Community Arts Project | Elyria, Ohio")

with help_col:
    # Minimalist Instructions Popover
    with st.popover("📖 Help"):
        st.markdown("""
        **Quick Start:**
        - **Upload**: Fill slots 1-8.
        - **Scale**: Use 'Fill' to bleed to edges.
        - **Spread**: Spans two slots.
        - **Print**: Use 'Actual Size' setting.
        """)

st.divider()

# Grid Layout: 2-wide on Desktop, 1-wide on Mobile (Standard Streamlit behavior)
for row_idx in range(1, 9, 2):
    col1, col2 = st.columns(2)
    with col1:
        page_card(row_idx)
    with col2:
        page_card(row_idx + 1)

st.divider()

# Generation Action
if st.button("🚀 Generate PDF for Printing", type="primary", use_container_width=True):
    ready_pages = {}
    layout_cols = {5:0, 4:1, 3:2, 2:3, 6:0, 7:1, 8:2, 1:3}
    
    pages_to_process = [n for n, d in st.session_state.pages.items() if d["image"]]
    
    if not pages_to_process:
        st.warning("Upload at least one image to begin.")
    else:
        with st.status("Calculating Imposition...", expanded=False) as status:
            # Points conversion for Letter Landscape
            slot_w = (11 * 72) / 4 
            slot_h = (8.5 * 72) / 2

            for i, num in enumerate(pages_to_process):
                data = st.session_state.pages[num]
                col = layout_cols[num]
                
                # Sync with the Generator's Absolute Math
                usable_h = slot_h - margin - (gutter / 2)
                if data.get("is_spread"):
                    usable_w = (slot_w * 2) - (margin * 2)
                else:
                    usable_w = slot_w - margin - (gutter / 2) if col in [0, 3] else slot_w - gutter

                processed_img, w, h = process_image(data["image"], data["scale_mode"], usable_w, usable_h)
                
                ready_pages[num] = {
                    "image": processed_img,
                    "display_size": (w, h),
                    "is_spread": data.get("is_spread")
                }
            
            pdf_bytes = create_zine_pdf(ready_pages, show_guides, project_title, margin, gutter)
            status.update(label="Zine Generated!", state="complete", expanded=False)

        st.download_button(
            label="📥 Download Ready-to-Print PDF",
            data=pdf_bytes,
            file_name=f"{project_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )