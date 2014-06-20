__author__ = 'alexander'

from robofab.world import OpenFont

d_font_filename = '/Users/alexander/Documents/WORKS/Paratype/ERBAR/ufo/PT-JSDB-Regular.ufo'
s_font_filename = '/Users/alexander/Documents/WORKS/Paratype/ERBAR/ufo/new 200414/PT-Emil-Regular.ufo'

d_font = OpenFont(d_font_filename)
s_font = OpenFont(s_font_filename)

for s_glyph in s_font:
	if not s_glyph.name in d_font:
		print 'Glyph %s not founded in %s' % (s_glyph.name, d_font)
		d_font.insertGlyph(s_glyph, s_glyph.name)
		print 'Imported...'

print 'DONE'
