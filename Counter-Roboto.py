cyan = (0.0, 0.953125, 1.0, 0.5)
orange = (1.0, 0.8, 0.4, 1.0)
blue = (0.4, 0.8, 1.0, 1.0)

listoffonts = AllFonts()
#print listoffonts
for font in listoffonts:
    cyancount = 0
    orangecount = 0
    bluecount = 0
    #font = CurrentFont()
    for glyph in font:
        if glyph.mark == cyan:
            cyancount +=1
        if glyph.mark == orange:
            orangecount +=1
        if glyph.mark == blue:
            bluecount +=1
    print font        
    print 'Cyan: %i / Orange: %i / SUM: %i / Blue: %i' % (cyancount, orangecount, cyancount+orangecount, bluecount)