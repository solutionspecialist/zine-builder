### agents.md

## Modular Architecture

To keep the codebase maintainable and "human-clean," we strictly enforce the separation of concerns:

1. **`engine.py`:** Headless logic only. Contains math, image processing (Pillow), and PDF generation (ReportLab). **Rule:** No Streamlit imports or widgets are allowed here.
2. **`ui.py`:** Contains all Streamlit layout logic, sidebar components, and page cards.
3. **`app.py`:** Connects the UI to the Engine. It handles the high-level flow and `st.session_state` orchestration.

## Zine Geometry & Imposition

The engine handles a standard 8-page "mini-zine" layout from a single 11" x 8.5" sheet.

### 1. The 8-Panel Orientation Map

Because the paper is folded, the layout requires specific structural flips:

* **Top Row (Pages 5, 4, 3, 2):** Inverted (rotated 180°) in the final PDF.
* **Bottom Row (Pages 6, 7, 8, 1):** Standard orientation (0°).
* **User Adjustments:** User-defined rotations (90° increments) are applied *after* these structural flips.

### 2. Physical Layout Math

* **Safe Area Calculation:** Page dimensions must dynamically update based on user-defined **Margins** (outer edges) and **Gutters** (internal fold lines).
* **DPI Standard:** Calculations assume 300 DPI for high-quality print exports, though UI previews may be lower for performance.

## Tech Stack & UX Standards

* **Image Processing:** Pillow (PIL) for normalization and filtering.
* **PDF Generation:** ReportLab for precise coordinate-based layout.
* **Mobile-First Design:** UI components must be optimized for mobile use. Controls should be accessible and clear.
* **Data Transparency:** The system is stateless by design. User data should be processed in memory and never persisted longer than the active session.