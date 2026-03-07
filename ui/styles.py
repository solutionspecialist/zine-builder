import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Modern Minimalist Base */
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
        
        /* Hover Effect for Interactive Feel */
        div[data-testid="column"]:hover {
            border-color: #58a6ff; /* Garford Blue accent */
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        /* Streamline Buttons */
        .stButton>button {
            border-radius: 8px;
            text-transform: uppercase;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        /* Hide redundant padding */
        .block-container {
            padding-top: 2rem;
            max-width: 1000px;
        }
        </style>
    """, unsafe_allow_html=True)