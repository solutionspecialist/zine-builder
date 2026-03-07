from PIL import Image
import io

def process_image(pil_img, scale_mode, target_w, target_h):
    # Work on a copy to keep the original state clean
    img = pil_img.copy()
    img_w, img_h = img.size
    
    # Calculate scale factor
    if scale_mode == "fit":
        scale = min(target_w / img_w, target_h / img_h)
    else: # fill
        scale = max(target_w / img_w, target_h / img_h)
        
    new_w, new_h = img_w * scale, img_h * scale
    
    # Pre-compressing for speed and smaller PDF size
    # JPEG at 85% with optimization is very fast for local processing
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    buf.seek(0)
    
    return Image.open(buf), new_w, new_h