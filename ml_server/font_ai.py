import sys, os
from fontTools.fontBuilder import FontBuilder

def create_dummy_font(output_path="public/output/output.ttf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fb = FontBuilder(1024, isTTF=True)
    fb.setupGlyphOrder([".notdef","A","B","C"])
    fb.setupCharacterMap({"A":"A","B":"B","C":"C"})
    fb.setupGlyf({})
    fb.setupHorizontalMetrics({})
    fb.setupHorizontalHeader()
    fb.setupOS2()
    fb.setupPost()
    fb.save(output_path)
    print("Font saved to", output_path)

if __name__ == "__main__":
    create_dummy_font()
