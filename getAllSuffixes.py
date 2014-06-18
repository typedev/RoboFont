__author__ = 'alexander'
font = CurrentFont()
fealist = []
print 'Available Suffixes in:', font
for g in font:
	name = g.name
	if '.' in name:
		a = name.split('.')
		gname = a[0]
		sfx = a[1]
		if '.' + sfx not in fealist:
			fealist.append('.' + sfx)
print fealist

for sfx in fealist:
	if sfx == '.notdef': break
	print '\nSuffix:', sfx
	for glyph in font:
		if sfx in glyph.name:
			print glyph.name

print '\nit may be liga:'
for glyph in font:
	if '_' in glyph.name:
		print glyph.name