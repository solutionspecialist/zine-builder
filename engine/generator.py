from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
import io

def create_zine_pdf(ready_pages, show_guides, project_title, margin, gutter):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # 1. Define the grid slots
    slot_w, slot_h = width / 4, height / 2

    # 2. THE IMPOSITION MAP (The missing 'layout')
    # Column (0-3), Row (0-1), Structural Flip (0 or 180)
    layout = {
        5: (0, 0, 180), 4: (1, 0, 180), 3: (2, 0, 180), 2: (3, 0, 180),
        6: (0, 1, 0),   7: (1, 1, 0),   8: (2, 1, 0),   1: (3, 1, 0)
    }
    
    spread_pairs = {8: 1, 6: 7, 4: 5, 2: 3}

    for page_num, (col, row, structural_flip) in layout.items():
        # Skip if this is a target page being covered by a spread
        if any(page_num == t and ready_pages.get(a, {}).get("is_spread") 
               for a, t in spread_pairs.items()):
            continue

        data = ready_pages.get(page_num)
        if not data: continue

        c.saveState()
        slot_x, slot_y = col * slot_w, (1 - row) * slot_h
        
        # Center Calculation
        if data.get("is_spread"):
            draw_width = slot_w * 2
            center_x = slot_x if page_num in [8, 2] else slot_x + slot_w
        else:
            draw_width = slot_w
            if col == 0:
                center_x = slot_x + (slot_w / 2) + (margin / 2) - (gutter / 2)
            elif col == 3:
                center_x = slot_x + (slot_w / 2) - (margin / 2) + (gutter / 2)
            else:
                center_x = slot_x + (slot_w / 2)
        
        center_y = slot_y + (slot_h / 2)

        # Draw the image
        c.translate(center_x, center_y)
        c.rotate(structural_flip)
        
        draw_w, draw_h = data["display_size"]
        c.drawImage(ImageReader(data["image"]), -draw_w/2, -draw_h/2, 
                    width=draw_w, height=draw_h, mask='auto')
        c.restoreState()

    # 3. Cut/Fold Guides
    if show_guides:
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setDash(3, 3)
        c.line(0, height/2, width, height/2) # Horizontal fold
        for i in range(1, 4): 
            c.line(i * slot_w, 0, i * slot_w, height) # Vertical folds

    c.showPage()
    c.save()
    packet.seek(0)
    return packet