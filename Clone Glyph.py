# RoboFont Script
# Dublicate selected glyphs and rename them to NameGlyph.XXX ( XXX - 001, 002 ... 999 ) 
# Alexander Lubovenko
# http://github.com/typedev

from robofab.world import CurrentFont, CurrentGlyph
from mojo.UI import *
from time import asctime

font = CurrentFont()
glyphslist = font.selection

def cloneGlyph(glyph,name=''):
    if name == '':
        oldname = glyph.name
    else:
        oldname = name
    for i in range(1,1000):
        newName = oldname+'.'+'%03d' % i
        if newName not in font.keys():
            font.insertGlyph(glyph,newName)
            font.update()
            font[newName].note = asctime()
            break

for i in glyphslist:
    glyph = font[i]
    lname = glyph.name.split('.')
    if len(lname) == 1:
        cloneGlyph(glyph)
    else:
        gnumber = lname[-1]
        if gnumber.isdigit():
            lname.pop()
            sname='.'.join(lname)
            cloneGlyph(glyph,sname)

font.update()