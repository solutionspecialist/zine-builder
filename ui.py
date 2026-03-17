import base64
from io import BytesIO

import streamlit as st
from PIL import Image, ImageOps


def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
        }
        
        /* De-cluttering Headers */
        h1 {
            font-weight: 700;
            letter-spacing: -1px;
            color: #ffffff;
        }
        
        /* Minimalist Card Container */
        div[data-testid="column"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.2s ease-in-out;
        }
        
        div[data-testid="column"]:hover {
            border-color: #58a6ff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .stButton>button {
            border-radius: 8px;
            text-transform: uppercase;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .block-container {
            padding-top: 2rem;
            max-width: 1000px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def show_help_modal():
    """Show a modal with templates and information."""
    modal_html = """
    <div style="position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background-color: rgba(0,0,0,0.7);">
        <div style="background-color: #0e1117; color:#ffffff; padding: 25px; border: 1px solid #30363d; border-radius: 12px; width: 90%; max-width: 600px; max-height: 80vh; overflow-y: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.5;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0; font-weight: 700; letter-spacing: -0.5px; color: #ffffff;">Zine Builder Help</h2>
            </div>
            
            <h3 style="font-weight: 600; color: #ffffff; margin-top: 20px; margin-bottom: 10px;">Page Dimensions</h3>
            <p style="color: #c9d1d9; margin-bottom: 15px;">Images will be cropped or centered to fit the pages, but for optimal appearance try the dimensions below:</p>
            <ul style="color: #c9d1d9; margin-bottom: 25px; padding-left: 20px;">
                <li>Single Pages should be approximately 825x1275 Pixels</li>
                <li>Spread Pages should be approximately 1650x1275 Pixels</li>
            </ul>
            <p style="color: #c9d1d9; margin-bottom: 25px;">Margins & Gutters will change this but you'll be close!</p>
            
            <h3 style="font-weight: 600; color: #ffffff; margin-top: 20px; margin-bottom: 10px;">Folding Instructions</h3>
            <ol style="color: #c9d1d9; margin-bottom: 25px; padding-left: 20px;">
                <li>Print the PDF single-sided</li>
                <li>Fold in half lengthwise (hot dog fold)</li>
                <li>Fold in half widthwise (hamburger fold)</li>
                <li>Fold one more time widthwise</li>
                <li>Unfold, then cut along center fold (red line of Fold Guide)</li>
                <li>Refold into your 8-page zine!</li>
                <li><a href="https://www.museums.cam.ac.uk/sites/default/files/how%20to%20fold%20a%20zine.pdf" target="_blank" style="color: #58a6ff; text-decoration: none;">Visual directions I found on the internet</a></li>
            </ol>
            
            <h3 style="font-weight: 600; color: #ffffff; margin-top: 20px; margin-bottom: 10px;">Tips for Best Results</h3>
            <ul style="color: #c9d1d9; margin-bottom: 25px; padding-left: 20px;">
                <li>Use images at least 1200x1800 pixels for good print quality</li>
                <li>"Fill" mode crops images to fit the page</li>
                <li>"Fit" mode shows the entire image with possible borders</li>
                <li>Test with regular paper before using nice paper</li>
            </ul>
            
            <h3 style="font-weight: 600; color: #ffffff; margin-top: 20px; margin-bottom: 10px;">Mobile Notes</h3>
            <ul style="color: #c9d1d9; margin-bottom: 25px; padding-left: 20px;">
                <li>Pick photos quickly to avoid timeouts</li>
                <li>Large photos may take longer to process</li>
                <li>Use landscape mode for easier navigation</li>
            </ul>
        </div>
    </div>
    """

    modal_container = st.container()
    with modal_container:
        st.components.v1.html(modal_html, height=650)


def sidebar_controls():
    st.sidebar.header("Zine Settings")

    st.sidebar.info("On mobile: Pick photos quickly to avoid timeouts")

    if st.sidebar.button("Help & Templates", use_container_width=True):
        st.session_state.show_help = True

    if st.session_state.get("show_help", False):
        show_help_modal()

        st.markdown(
            """
        <script>
        // Listen for close event from the modal
        window.addEventListener('message', function(event) {
            if (event.data.type === 'closeHelpModal') {
                // Trigger a Streamlit rerun to close the modal
                const closeEvent = new CustomEvent('closeHelpModalTrigger');
        </script>
        """,
            unsafe_allow_html=True,
        )

        if st.sidebar.button("Close Help", type="secondary", use_container_width=True):
            st.session_state.show_help = False
            st.rerun()

    project_title = st.sidebar.text_input(
        "Zine Title", value=st.session_state.get("project_title", "My Zine")
    )
    st.session_state.project_title = project_title

    st.sidebar.divider()
    st.sidebar.header("Page Layout")

    margin_inches = st.sidebar.slider(
        "External Margin (inches)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get("margin_inches", 0.0),
        step=0.05,
        help="White space around the entire 8-page sheet edge.",
    )

    gutter_px = st.sidebar.slider(
        "Internal Gutter (pixels)",
        min_value=0,
        max_value=15,
        value=st.session_state.get("gutter_px", 4),
        step=1,
        help="White space between individual pages for folding.",
    )

    show_guides = st.sidebar.toggle(
        "Show Fold Guides", value=st.session_state.get("show_guides", True)
    )

    st.sidebar.divider()

    if st.sidebar.button("Reset All Slots", type="secondary", use_container_width=True):
        st.session_state.pages = {
            i: {"image": None, "rotation": 0, "scale_mode": "fill", "is_spread": False}
            for i in range(1, 9)
        }
        st.rerun()

    st.session_state.margin_inches = margin_inches
    st.session_state.gutter_px = gutter_px
    st.session_state.show_guides = show_guides

    return margin_inches, gutter_px, project_title, show_guides


def image_to_base64(img):
    """Converts PIL image to base64 for browser-safe preview."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def handle_upload(page_num):
    """Handle image upload for a specific page."""
    v = st.session_state.get(f"v_{page_num}", 0)
    uploader_key = f"u_{page_num}_v{v}"

    uploaded_file = st.session_state.get(uploader_key)

    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            img = ImageOps.exif_transpose(img).convert("RGBA")
            img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)

            st.session_state.pages[page_num]["image"] = img
            st.toast("✅ Image processed!")
        except Exception as e:
            st.error(f"Error: {e}")


def toggle_spread(page_num):
    """Switches between single page and 2-page spread mode."""
    st.session_state.pages[page_num]["is_spread"] = not st.session_state.pages[
        page_num
    ]["is_spread"]


def page_card(page_num):
    """Renders the UI card for an individual zine page."""
    if f"v_{page_num}" not in st.session_state:
        st.session_state[f"v_{page_num}"] = 0

    page_data = st.session_state.pages[page_num]

    # Check if this page is 'covered' by a spread from a previous page
    is_covered = False
    if page_num == 8:
        if st.session_state.pages[1].get("is_spread"):
            is_covered = True
    elif page_num in [3, 5, 7]:
        if st.session_state.pages[page_num - 1].get("is_spread"):
            is_covered = True

    st.markdown(f"### Page {page_num}")

    with st.container(border=True):
        if is_covered:
            source = 1 if page_num == 8 else page_num - 1
            st.info(f"🔗 Linked to Page {source}")
            st.markdown(
                "<div style='height: 300px; display: flex; align-items: center; justify-content: center; font-size: 3rem; opacity: 0.1;'>🔗</div>",
                unsafe_allow_html=True,
            )

        elif page_data["image"]:
            img_b64 = image_to_base64(page_data["image"])
            st.markdown(
                f"""
                <div style="height: 300px; width: 100%; display: flex; justify-content: center; align-items: center; background-color: #1a1c24; overflow: hidden; border-radius: 8px; margin-bottom: 12px; border: 1px solid #333;">
                    <img src="data:image/png;base64,{img_b64}" style="max-height: 100%; max-width: 100%; object-fit: contain;">
                </div>
            """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "🔄 Rotate", key=f"rot_{page_num}", use_container_width=True
                ):
                    current_rotation = st.session_state.pages[page_num].get(
                        "rotation", 0
                    )
                    new_rotation = (current_rotation - 90) % 360
                    st.session_state.pages[page_num]["rotation"] = new_rotation
                    if page_data["image"]:
                        st.session_state.pages[page_num]["image"] = page_data[
                            "image"
                        ].rotate(-90, expand=True)
                    st.rerun()

                mode = "fill" if page_data["scale_mode"] == "fit" else "fit"
                btn_label = "✂️ Use Fill" if mode == "fill" else "🖼️ Use Fit"
                if st.button(
                    btn_label, key=f"mode_{page_num}", use_container_width=True
                ):
                    st.session_state.pages[page_num]["scale_mode"] = mode
                    st.rerun()

            with col2:
                if st.button(
                    "🗑️ Clear", key=f"clr_{page_num}", use_container_width=True
                ):
                    st.session_state.pages[page_num]["image"] = None
                    st.session_state.pages[page_num]["is_spread"] = False
                    st.session_state[f"v_{page_num}"] += 1
                    st.rerun()

                if page_num in [1, 2, 4, 6]:
                    target = 8 if page_num == 1 else page_num + 1
                    label = (
                        "Wraparound Cover"
                        if page_num == 1
                        else f"Spread to Page {target}"
                    )
                    st.checkbox(
                        label,
                        key=f"chk_spread_{page_num}",
                        value=page_data.get("is_spread", False),
                        on_change=toggle_spread,
                        args=(page_num,),
                    )
        else:
            st.markdown(
                """
                <div style='height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; 
                background-color: #0e1117; border: 1px dashed #444; border-radius: 8px; color: #666;'>
                <span style='font-size: 2rem; margin-bottom: 10px;'>📸</span>
                <span>Select Page Image</span>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.file_uploader(
                "Upload",
                type=["jpg", "jpeg", "png", "webp"],
                key=f"u_{page_num}_v{st.session_state[f'v_{page_num}']}",
                on_change=handle_upload,
                args=(page_num,),
                label_visibility="collapsed",
            )
