font = CurrentFont()
total = len(font)
count = total
for glyph in font:
    print '%i/%i %s' % (count, total, glyph.name)
    glyph.removeOverlap()
    glyph.update()
    count -= 1
print 'Done..'