import streamlit as st
from ui.sidebar import sidebar_controls 
from ui.cards import page_card
from ui.styles import apply_custom_css
from engine.generator import create_zine_pdf

# At the top of app.py
print("--- APP REFRESHED ---")
if "pages" in st.session_state:
    print(f"Current v_1: {st.session_state.get('v_1')}")

st.set_page_config(page_title="Garford Zine Builder", layout="centered")
apply_custom_css()

if "pages" not in st.session_state:
    st.session_state.pages = {
        i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False} 
        for i in range(1, 9)
    }

margin_inches, gutter_px, project_title, show_guides = sidebar_controls()

# Main UI
st.title("Garford Zine Builder")
st.caption("Lorain County Community Arts Project | Elyria, Ohio")
st.divider()

for row_idx in range(1, 9, 2):
    col1, col2 = st.columns(2)
    with col1: page_card(row_idx)
    with col2: page_card(row_idx + 1)

st.divider()

if st.button("🚀 Generate PDF for Printing", type="primary", use_container_width=True):
    pages_to_process = {n: d for n, d in st.session_state.pages.items() if d["image"]}
    
    if not pages_to_process:
        st.warning("Upload at least one image to begin.")
    else:
        with st.status("Generating Print-Ready Layout...", expanded=False) as status:
            pdf_bytes = create_zine_pdf(
                pages_to_process, 
                show_guides, 
                project_title, 
                margin_inches, 
                gutter_px
            )
            status.update(label="Zine Generated!", state="complete", expanded=False)

        st.download_button(
            label="📥 Download Ready-to-Print PDF",
            data=pdf_bytes,
            file_name=f"{project_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )