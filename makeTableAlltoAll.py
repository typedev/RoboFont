font = CurrentFont()

listglyphs = font.selection

result = ''

for b in listglyphs:
    gb = font[b].unicode
    for i in listglyphs:
        gi = font[i].unicode
        result = result + unichr(gb) + unichr(gi)
    result = result + '\n'
	
print result
		