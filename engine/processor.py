from PIL import Image
import io

def process_image(pil_img, scale_mode, target_w, target_h):
    # Work on a copy to keep original state clean
    img = pil_img.copy()
    img_w, img_h = img.size
    
    # Calculate scale factor based on target dimensions
    if scale_mode == "fit":
        scale = min(target_w / img_w, target_h / img_h)
    else: # fill
        scale = max(target_w / img_w, target_h / img_h)
        
    new_w, new_h = img_w * scale, img_h * scale
    
    # Pre-compressing for speed and smaller PDF size
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    buf.seek(0)
    
    return Image.open(buf), new_w, new_h