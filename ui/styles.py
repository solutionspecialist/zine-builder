import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Card Container - Theme Neutral */
        [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
            border: 1px solid rgba(128, 128, 128, 0.3);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
        }

        /* Stability for the Preview Box */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(128, 128, 128, 0.05);
        }

        /* Mobile Optimization */
        @media (max-width: 800px) {
            /* Force columns to 100% width so they stack in row-order */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
            
            /* Center text and buttons for thumb-friendly mobile use */
            [data-testid="column"] * {
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            
            .stButton button {
                width: 80% !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)