font = CurrentFont()
for guide in font.guides:
    font.removeGuide(guide)
for glyph in font:
    for guide in glyph.guides:
        glyph.removeGuide(guide)   