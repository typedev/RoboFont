from mojo.events import addObserver
from afiiTabl import *


def renameToAfiiCyrl(glyphName):
    if 'uni' in glyphName:
        n = getCyrlLetter(uName=glyphName)
        if n:
            print 'Glyph', n[uniN], 'renamed to', n[afiiN], '-Note:', n[noteCyrl]
            glyphName = n[afiiN]
    return glyphName
        
def checkGlyphNames(font):
    print "=== Rename glyphs from uniXXXX to afiiXXXXX ==="
    glyphChanged = False
    for glyph in font:
        oldGlyphName = glyph.name
        newGlyphName = renameToAfiiCyrl(glyph.name)
        if oldGlyphName != newGlyphName:
            font.renameGlyph(oldGlyphName, newGlyphName)
            font[newGlyphName].update()
            glyphChanged = True
            #font.update()   
    print "=== done renaming glyph names ==="
    if glyphChanged:
        print "=== Clearing GlyphOrder ==="
        font.glyphOrder = []
    print "===DONE==="
    
def checkGroupNames(font):
    print "=== Checking Group Names for Single Quotes ==="
    for groupName, items in font.groups.items():
        newItems = []
        for glyphName in items:
            if "'" in glyphName:
                glyphName = glyphName.replace("'", "")
                print glyphName,' changed'
            #glyphName = renameToAfiiCyrl(glyphName)    
            newItems.append(glyphName)
    
        if newItems != items:
            ## something changed
            font.groups[groupName] = newItems
    font.lib['com.typedev.markers.groupsclear'] = 'Cleared'
    print "=== done checking group names ==="
    


class RenameGroupsObserver(object):
    
    def __init__(self):
        addObserver(self, "checkFontNames", "fontDidOpen")
        
    def checkFontNames(self, info):
        font = info["font"]
        # print font.lib['com.typedev.markers.groupsok']
        if font.lib.has_key('com.typedev.markers.groupsclear'):
            print "=== Groups OK ==="
        else:
            checkGroupNames(font) 
            font.update()
        #checkGlyphNames(font)
        #font.glyphOrder = glyphOrder                
        

        


RenameGroupsObserver()