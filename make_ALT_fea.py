from robofab.world import CurrentFont

font = CurrentFont()

sfx_names = []
print 'Available Suffixes in:', font
for glyph in font:
	name = glyph.name
	if ('.' in name) and (name != '.notdef'):
		a = name.split('.')
		gname = a[0]
		sfx = a[1]
		if '.' + sfx not in sfx_names:
			sfx_names.append('.' + sfx)
print sfx_names

aaltdic = {}
for glyph in font:
	if ('.' in glyph.name) and (glyph.name != '.notdef'):
		a = glyph.name.split('.')
		gname = a[0]
		if gname not in aaltdic:
			aaltdic[gname] = [ '%s.' % gname + '.'.join(a[1:])]
		else:
			aaltdic[gname].append( '%s.' % gname + '.'.join(a[1:]))

print 'feature aalt {'
for name, alts in sorted(aaltdic.items()):
	print '\tsub %s from [ %s ];' % (name, ' '.join(alts))
print '} aalt;'
