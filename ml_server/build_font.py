import fontforge
import os

def build_font(svg_dir, out_ttf):
    font = fontforge.font()
    font.encoding = 'UnicodeFull'
    for fname in os.listdir(svg_dir):
        if not fname.endswith('.svg'): continue
        # 파일명 규칙: U+XXXX.svg or charname.svg
        glyphname = os.path.splitext(fname)[0]
        glyph = font.createChar(ord(glyphname)) 
        glyph.importOutlines(os.path.join(svg_dir, fname))
        glyph.width = 1000
    font.generate(out_ttf)
