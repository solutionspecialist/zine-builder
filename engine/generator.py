from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import io

def create_zine_pdf(ready_pages, show_guides, project_title, margin_inches, gutter_px):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=landscape(letter))
    c.setTitle(project_title)
    c.setAuthor("Steven Riggle")

    width, height = landscape(letter)
    slot_w, slot_h = width / 4, height / 2
    
    ext_margin = margin_inches * inch
    gut = gutter_px

    layout = {
        5: (0, 0, 180), 4: (1, 0, 180), 3: (2, 0, 180), 2: (3, 0, 180),
        6: (0, 1, 0),   7: (1, 1, 0),   8: (2, 1, 0),   1: (3, 1, 0)
    }
    
    links = {1: 8, 2: 3, 4: 5, 6: 7}
    processed_targets = []

    for page_num in [5, 4, 3, 2, 6, 7, 1, 8]:
        if page_num in processed_targets or page_num not in ready_pages:
            continue

        data = ready_pages[page_num]
        if not data.get("image"):
            continue

        img_reader = ImageReader(data["image"])
        img_w, img_h = img_reader.getSize()
        col, row, rot = layout[page_num]
        is_fill = data.get("scale_mode") == "fill"
        
        is_spread = data.get("is_spread") and page_num in links
        if is_spread:
            processed_targets.append(links[page_num])
            target_col = 0 if col in [0, 1] else 2
            col_span = 2
        else:
            target_col = col
            col_span = 1

        x_start, x_end = target_col * slot_w, (target_col + col_span) * slot_w
        y_start, y_end = (1 - row) * slot_h, (2 - row) * slot_h

        # Margin/Gutter logic
        if target_col == 0: x_start += ext_margin
        else: x_start += gut / 2
            
        if (target_col + col_span) == 4: x_end -= ext_margin
        else: x_end -= gut / 2
            
        if row == 1:
            y_start += ext_margin
            y_end -= gut / 2
        else:
            y_start += gut / 2
            y_end -= ext_margin

        safe_w, safe_h = x_end - x_start, y_end - y_start
        center_x, center_y = x_start + safe_w / 2, y_start + safe_h / 2

        scale = max(safe_w/img_w, safe_h/img_h) if is_fill else min(safe_w/img_w, safe_h/img_h)
        draw_w, draw_h = img_w * scale, img_h * scale
        draw_x, draw_y = center_x - draw_w / 2, center_y - draw_h / 2

        c.saveState() 
        clip_path = c.beginPath()
        clip_path.rect(x_start, y_start, safe_w, safe_h)
        c.clipPath(clip_path, stroke=0, fill=0)

        c.saveState()
        if rot == 180:
            c.translate(center_x, center_y)
            c.rotate(180)
            c.translate(-center_x, -center_y)
            
        c.drawImage(img_reader, draw_x, draw_y, width=draw_w, height=draw_h, preserveAspectRatio=True)
        c.restoreState()
        c.restoreState()

    if show_guides:
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setDash(2, 2)
        for i in range(1, 4): c.line(i * slot_w, 0, i * slot_w, height)
        c.line(0, slot_h, width, slot_h)
        c.setDash()
        c.setStrokeColorRGB(1, 0, 0)
        c.line(slot_w, slot_h, slot_w * 3, slot_h)

    c.showPage()
    c.save()
    return packet.getvalue()