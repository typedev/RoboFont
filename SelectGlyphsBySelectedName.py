__author__ = 'alexander'


stroke = ''
font = CurrentFont()
stroke = []

base = font.selection[0]
# group = '@MMK_L_%s' % base
# print 'A %s' % group
for g in font:
	if g.name.startswith(base):
		stroke.append(g.name)
# print sss
stroke.sort()

print ' '.join(stroke)
# print a