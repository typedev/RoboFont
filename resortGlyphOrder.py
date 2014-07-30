font = CurrentFont()

sortedlist = sorted(font.selection)

glyphOrder = font.lib[ 'public.glyphOrder' ]

indexes = []
start = None

for name in font.selection:
	for id, fglyph in enumerate(glyphOrder):
		if fglyph == name:
			indexes.append(id)

for id, index in enumerate(indexes):
	print glyphOrder[index], ' << ', sortedlist[id]
	glyphOrder[index]= sortedlist[id]
	font[sortedlist[id]].update()

font.lib['public.glyphOrder'] = glyphOrder
font.glyphOrder = font.lib['public.glyphOrder']
font.update()