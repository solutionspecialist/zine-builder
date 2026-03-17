# 🚀 Deployment Guide: Garford Zine Builder

This app is designed to be hosted on **Streamlit Community Cloud**.

## 1. Prerequisites
- The repository must be public on GitHub.
- `requirements.txt` must be in the root directory.
- `app.py` must be in the root directory.

## 2. Launching on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account.
3. Click **"New app"**.
4. Select this repository (`garford-zine-builder`).
5. Set the Main file path to `app.py`.
6. Click **"Deploy!"**.

## 3. Post-Deployment Settings
- **Theme:** In the app settings on Streamlit Cloud, set the theme to "Light" or "Dark" to ensure the custom CSS in `ui/styles.py` renders consistently across mobile devices.
- **Resources:** This app processes images in memory. If the app crashes during large uploads, check the "Manage app" console for memory limit errors.

## 4. Troubleshooting
- **Missing Module:** If the app fails to start, ensure all libraries (Pillow, reportlab) are listed in `requirements.txt`.
- **Layout Issues:** Ensure `ui/` and `engine/` folders were pushed to GitHub, not just the root files.