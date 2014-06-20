
from robofab.world import CurrentFont, RFont, OpenFont

s_font_name = 'Roboto_Bold_140515.vfb'
d_font_name = 'Roboto_Bold.vfb'

general_path = '/Users/alexander/Documents/WORKS/Paratype/Roboto_180614/'
source_font_path = general_path + 'OLD/' + s_font_name
dest_font_path = general_path + d_font_name

s_font = OpenFont(source_font_path)
d_font = OpenFont(dest_font_path)
print 'Source:', s_font
print 'Dest:', d_font


def glyphHasAnchor (glyph):
	if len(glyph.anchors) > 0:
		return True
	else:
		return False

def anchorNameExist(glyph, anchorname):
	for anchor in glyph.anchors:
		if anchorname == anchor.name:
			return True
	return False

def printListOfAnchors(glyph):
	for anchor in glyph.anchors:
		print '\t',anchor.index, anchor.name, anchor.position

def importAnchors(source_glyph, dest_glyph):

	for s_anchor in source_glyph.anchors:
		if not anchorNameExist(dest_glyph, s_anchor.name):
			print s_anchor.name, 'NOT FOUND in', d_font_name, dest_glyph.name, 'IT WILL BE IMPORTED'

############# FONTLAB Section ONLY BEGIN
			anch = Anchor(s_anchor.name, s_anchor.x, s_anchor.y)
			g = fl.font[fl.font.FindGlyph(dest_glyph.name)]
			g.anchors.append(anch)
			g.mark = 25
			fl.UpdateFont()
############# FONTLAB Section ONLY END

			# d_font[dest_glyph.name].anchors.append(anch)
			# d_font[dest_glyph.name].mark = 20
			# d_font[dest_glyph.name].update()
			print s_anchor.name, 'ADDED..'

		else:
			print s_anchor.name, 'availabe in', d_font_name, dest_glyph.name, 'nothing changed'





for s_glyph in s_font:
	if glyphHasAnchor(s_glyph):
		print s_font_name, s_glyph.name#, s_glyph.anchors
		printListOfAnchors(s_glyph)
		if d_font.has_key(s_glyph.name):
			if glyphHasAnchor(d_font[s_glyph.name]):
				# print '#########'
				print d_font_name, s_glyph.name#, d_font[s_glyph.name].anchors
				printListOfAnchors(d_font[s_glyph.name])
				importAnchors(s_glyph, d_font[s_glyph.name])
				printListOfAnchors(d_font[s_glyph.name])
			else:
				print d_font_name, s_glyph.name, 'anchors not found'
				importAnchors(s_glyph, d_font[s_glyph.name])
				printListOfAnchors(d_font[s_glyph.name])
		else:
			print 'WARNING!', d_font_name, s_glyph.name, 'glyph not found'
d_font.update()