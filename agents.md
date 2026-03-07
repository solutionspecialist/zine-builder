# Agent Context & System Rules: Garford Zine Builder
**Project Version:** 2.0 (Stable Layout & DIY Ethos)

## 🏗 Architecture Rules
1. **Strict Separation:** Never put Streamlit widgets (`st.button`, etc.) inside the `engine/` folder. Logic must remain headless.
2. **Data Flow:** UI collects bytes -> Engine processes/scales -> UI displays preview -> Generator builds PDF.
3. **Source of Truth:** Use `st.session_state.pages` for all 8 slots. Initialization must default to `scale_mode: "fill"`.

## 📐 Zine Geometry & Imposition
The project uses a standard 8-page "mini-zine" fold from a single 11" x 8.5" sheet.

### 1. Orientation Map
- **Top Row (Pages 5, 4, 3, 2):** Must be structurally flipped 180° in the PDF.
- **Bottom Row (Pages 6, 7, 8, 1):** Orientation is 0°.
- **User Rotations:** Applied on top of structural flips in 90° increments.

### 2. Physical Layout Math (72 DPI)
- **Slot Dimensions:** 2.75" x 4.25" (198px x 306px).
- **Margins:** Applied only to outer paper edges (Top, Bottom, Left, Right).
- **Gutters:** Applied to internal fold lines.
- **Side-Aware Logic:** - Columns 0 & 3 (Edges) subtract 1 Margin + 1 Gutter.
  - Columns 1 & 2 (Folds) subtract 2 Gutters (0 Margin).

## 🎨 UI & UX Standards
- **Mobile-First:** Ensure slot controls are large enough for thumb-taps at the Arts Fest station.
- **Visual Lockout:** If a spread is active (2-3, 4-5, 6-7, 8-1), the target page must be visually disabled in `ui/cards.py`.
- **Clean Interface:** Use `data-testid="stFileUploaderFile"` CSS injection to hide file metadata/filenames for a "Photo Booth" feel.
- **Metadata:** PDF filenames must be slugified from the `project_title` session variable.

## 🛠 Tech Stack
- **Frontend:** Streamlit (Wide Mode)
- **Image Processing:** Pillow (PIL)
- **PDF Engine:** ReportLab