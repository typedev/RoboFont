
from robofab.world import CurrentFont

def glyphHasAnchor (glyph):
	if len(glyph.anchors) > 0:
		return True
	else:
		return False


font = CurrentFont()
print font
for glyph in font:
	if glyphHasAnchor(glyph):
		print glyph.name, glyph.anchors