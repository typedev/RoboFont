__author__ = 'alexander'

stroke = ''
font = CurrentFont()

for g in font.selection:
	g = g.replace('\n','')
	stroke = stroke + g + ' '
print stroke
