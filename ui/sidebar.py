import streamlit as st

def sidebar_controls():
    st.sidebar.header("🛠️ Station Settings")
    
    # 1. Project Title
    project_title = st.sidebar.text_input(
        "Zine Title", 
        value=st.session_state.get('project_title', "Garford Fest 2026")
    )
    st.session_state.project_title = project_title
    
    st.sidebar.divider()
    st.sidebar.header("📐 Global Layout")
    
    # 2. External Margin: 0.0" to 1.0" in 0.05" steps
    margin_inches = st.sidebar.slider(
        "External Margin (inches)", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.get('margin_inches', 0.0),
        step=0.05,
        help="White space around the entire 8-page sheet edge."
    )
    
    # 3. Internal Gutters: 0px to 15px in 1px steps
    gutter_px = st.sidebar.slider(
        "Internal Gutter (pixels)", 
        min_value=0, 
        max_value=15, 
        value=st.session_state.get('gutter_px', 4),
        step=1,
        help="White space between individual pages for folding."
    )
    
    # 4. Fold Guides Toggle
    show_guides = st.sidebar.toggle(
        "Show Fold Guides", 
        value=st.session_state.get('show_guides', True)
    )

    st.sidebar.divider()
    
    # Global Reset Button
    if st.sidebar.button("🗑️ Reset All Slots", type="secondary", use_container_width=True):
        st.session_state.pages = {
            i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False} 
            for i in range(1, 9)
        }
        st.rerun()

    # Store in session state for the generator to access
    st.session_state.margin_inches = margin_inches
    st.session_state.gutter_px = gutter_px
    st.session_state.show_guides = show_guides
    
    # Return all 4 values to resolve the Unpack Error
    return margin_inches, gutter_px, project_title, show_guides