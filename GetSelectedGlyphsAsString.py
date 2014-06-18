__author__ = 'alexander'

stroke = ''
font = CurrentFont()

for g in font.selection:
	stroke = stroke + g + ' '
print stroke
