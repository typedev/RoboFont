gselected = CurrentGlyph()

print 'Selected glyph: ', gselected.name, 'marked as', gselected.mark
names = []
for gf in CurrentFont():
	if gf.mark == gselected.mark:
		names.append(gf.name)
print names
namesstr = ''
for n in names:
	namesstr = namesstr + n +' '
print namesstr
