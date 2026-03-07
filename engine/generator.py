from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
import io

def create_zine_pdf(ready_pages, show_guides, project_title, margin, gutter):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(letter))
    
    # --- METADATA FIX ---
    # This removes the 'Untitled' title in PDF viewers and browsers
    c.setTitle(project_title)
    c.setAuthor("Arthur Garford")
    c.setSubject("Garford Arts Fest")
    # --------------------

    width, height = landscape(letter)
    slot_w, slot_h = width / 4, height / 2

    # Row 1 is Top (flipped), Row 0 is Bottom
    layout = {
        5: (0, 1, 180), 4: (1, 1, 180), 3: (2, 1, 180), 2: (3, 1, 180),
        6: (0, 0, 0),   7: (1, 0, 0),   8: (2, 0, 0),   1: (3, 0, 0)
    }
    
    spread_pairs = {8: 1, 6: 7, 4: 5, 2: 3}

    for page_num, (col, row, structural_flip) in layout.items():
        if any(page_num == t and ready_pages.get(a, {}).get("is_spread") for a, t in spread_pairs.items()):
            continue

        data = ready_pages.get(page_num)
        if not data: continue

        # --- 1. DEFINE THE BOUNDARY BOX (The "Clip" Area) ---
        # Start with the raw slot
        box_x = col * slot_w
        box_y = row * slot_h
        box_w = slot_w
        box_h = slot_h

        # Apply Outer Margins
        if col == 0: box_x += margin; box_w -= margin
        if col == 3: box_w -= margin
        if row == 1: box_h -= margin # Top edge of paper
        if row == 0: box_y += margin; box_h -= margin # Bottom edge of paper

        # Apply Inner Gutters (The Folds)
        if not data.get("is_spread"):
            if col == 0: box_w -= (gutter / 2)
            elif col == 3: box_x += (gutter / 2); box_w -= (gutter / 2)
            else: box_x += (gutter / 2); box_w -= gutter
        
        # Horizontal Fold Gutter
        if row == 1: box_y += (gutter / 2); box_h -= (gutter / 2)
        else: box_h -= (gutter / 2)

        # --- 2. DRAWING WITH FORCED CLIPPING ---
        c.saveState()
        
        # Create the clipping path BEFORE any translations
        clip_path = c.beginPath()
        clip_path.rect(box_x, box_y, box_w, box_h)
        c.clipPath(clip_path, stroke=0)

        # Move to the center of the calculated box
        cx, cy = box_x + (box_w / 2), box_y + (box_h / 2)
        c.translate(cx, cy)
        c.rotate(structural_flip)
        
        draw_w, draw_h = data["display_size"]
        c.drawImage(ImageReader(data["image"]), -draw_w/2, -draw_h/2, 
                    width=draw_w, height=draw_h, mask='auto')
        
        c.restoreState()

    if show_guides:
        c.setStrokeColorRGB(0, 0, 1)
        c.setDash(1, 3)
        c.line(0, height/2, width, height/2)
        for i in range(1, 4): c.line(i * slot_w, 0, i * slot_w, height)

    c.showPage()
    c.save()
    packet.seek(0)
    return packet