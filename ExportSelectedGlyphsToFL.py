import sys

sys.path.append( '/Users/alexander/PycharmProjects/CustomControls' )

import tdReport
from robofab.world import CurrentFont, CurrentGlyph
font = CurrentFont()
gselected = CurrentGlyph()

TOFL_MARK = (0.4, 1.0, 0.4, 1.0)
EXPORTED = (0.4, 1.0, 0.4, 0.1)
EXCEPT_MARK = (1.0, 0.8, 0.4, 1.0)

file_ext = 'toFl'
path_exp = font.path.replace('.ufo','')
# filename = font.filename
report = tdReport.Report(file = path_exp, ext = 'toFL', process= 'Export selected glyphs to FontLab' )
print 'Selected glyph: ', gselected.name, 'marked as', gselected.mark
names = []
for gf in CurrentFont():
	if gf.mark == gselected.mark:
		names.append(gf.name)
		report.add(gf.name)
print names
print 'Glyph list saved as: ' + path_exp + '.' + file_ext
report.save()


