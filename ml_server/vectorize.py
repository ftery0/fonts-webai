import potrace
import numpy as np
from PIL import Image

def bitmap_to_svg(in_path, out_path_svg):
    im = Image.open(in_path).convert('L')
    bw = im.point(lambda p: 0 if p>128 else 1, '1')  
    arr = np.array(bw, dtype=np.uint8)
    bmp = potrace.Bitmap(arr)
    path = bmp.trace()
    with open(out_path_svg, 'w') as f:
        f.write('<?xml version="1.0" standalone="no"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
        for curve in path:
            for c in curve:
                
                f.write('<path d="..."/>')
        f.write('</svg>')
