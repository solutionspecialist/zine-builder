from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
import io

def create_zine_pdf(pages_data, show_guides, project_title, margin, gutter):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(letter))
    width, height = landscape(letter)
    slot_w, slot_h = width / 4, height / 2

    layout = {
        5: (0, 0, 180), 4: (1, 0, 180), 3: (2, 0, 180), 2: (3, 0, 180),
        6: (0, 1, 0),   7: (1, 1, 0),   8: (2, 1, 0),   1: (3, 1, 0)
    }
    spread_pairs = {8: 1, 6: 7, 4: 5, 2: 3}

    for page_num, (col, row, structural_flip) in layout.items():
        data = pages_data.get(page_num)
        
        if any(page_num == t and pages_data.get(a, {}).get("is_spread") for a, t in spread_pairs.items()):
            continue
        if not data or not data.get("image"):
            continue

        c.saveState()
        slot_x, slot_y = col * slot_w, (1 - row) * slot_h 
        
        if data.get("is_spread"):
            clip_x = (slot_w * 2) if page_num in [8, 2] else 0
            clip_w = slot_w * 2
            center_x = (slot_w * 3) if page_num in [8, 2] else (slot_w * 1)
        else:
            clip_x, clip_w = slot_x, slot_w
            
            # Anchor Logic:
            # Shift the image center to account for the margin being on only one side
            if col == 0: # Left edge: Margin left, Gutter right
                center_x = slot_x + (slot_w / 2) + (margin / 2) - (gutter / 2)
            elif col == 3: # Right edge: Gutter left, Margin right
                center_x = slot_x + (slot_w / 2) - (margin / 2) + (gutter / 2)
            else: # Inner slots: Gutters on both sides
                center_x = slot_x + (slot_w / 2)

        center_y = slot_y + (slot_h / 2)

        path = c.beginPath()
        path.rect(clip_x, slot_y, clip_w, slot_h)
        c.clipPath(path, stroke=0)

        c.translate(center_x, center_y)
        c.rotate(structural_flip)
        
        draw_w, draw_h = data["display_size"]
        c.drawImage(ImageReader(data["image"]), -draw_w/2, -draw_h/2, width=draw_w, height=draw_h, mask='auto')
        c.restoreState()

    if show_guides:
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setDash(3, 3)
        c.line(0, height/2, width, height/2)
        for i in range(1, 4): c.line(i * slot_w, 0, i * slot_w, height)
        c.setDash([])
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(1.2)
        c.line(slot_w, height/2, slot_w * 3, height/2)

    c.showPage()
    c.save()
    packet.seek(0)
    return packet