from PIL import Image, ImageOps
import io

def process_image(image_bytes, rotation_angle, scale_mode, target_w, target_h):
    img = Image.open(image_bytes)
    img = ImageOps.exif_transpose(img) 
    img = img.convert("RGB")
    
    if rotation_angle != 0:
        img = img.rotate(-rotation_angle, expand=True)
    
    img_w, img_h = img.size
    
    if scale_mode == "fit":
        # Fit to the NEW target width (which is slot_w * 2 for spreads)
        scale = min(target_w / img_w, target_h / img_h)
    else: # "fill"
        scale = max(target_w / img_w, target_h / img_h)
        
    new_w, new_h = img_w * scale, img_h * scale
    
    # Return processed image as BytesIO for ReportLab
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    
    return buf, new_w, new_h