
import colorsys

f = CurrentFont()

MASK_LIB_KEY = "org.robofab.fontlab.maskData"
MARK_LIB_KEY = "org.robofab.fontlab.mark"

def portFLmark(glyph):
    fontLabMarkColor = 0
    fontLabMarkColor = glyph.lib.get("org.robofab.fontlab.mark")
    if fontLabMarkColor != 0:
        r, g, b = colorsys.hsv_to_rgb(fontLabMarkColor/256., 1., 1.)
        glyph.mark = (r, g, b, .5)
        

def portFLmaskData(glyph):
    #get pendata
    # filter out any single point contours (anchors)
    instructions = []
    pointStack = []
    lib = glyph.lib
    
    if lib.has_key(MASK_LIB_KEY):
        instructions = lib[MASK_LIB_KEY]
        pen = glyph.getPointPen()
        instructionsDrawPoints(instructions, pen)
        # clear the mask data from the glyph lib
        del lib[MASK_LIB_KEY]
    glyph.update()

def instructionsDrawPoints(instructions, pointPen):
    """draw instructions created by InstructionPointPen"""
    # filter out single point contours (anchors)
    pointStack = []
    for instruction in instructions:
        pointStack.append(instruction)
        meth = instruction["method"]
        if meth == "endPath":
            if len(pointStack) > 3:
                _drawPointStack(pointStack, pointPen)
            pointStack = []
            
def _drawPointStack(stack, pointPen):
    for instruction in stack:
        meth = instruction["method"]
        if meth == "beginPath":
            pointPen.beginPath()
        elif meth == "endPath":
            pointPen.endPath()
        elif meth == "addPoint":
            pt = instruction["pt"]
            smooth = instruction.get("smooth")
            segmentType = instruction.get("segmentType")
            name = instruction.get("name")
            pointPen.addPoint(pt, segmentType, smooth, name)
        elif meth == "addComponent":
            baseGlyphName = instruction["baseGlyphName"]
            transformation = instruction["transformation"]
            pointPen.addComponent(baseGlyphName, transformation)
        else:
            raise NotImplementedError, meth

for glyph in f:
    #port the colour marks
    portFLmark(glyph)
    #create/get the layer for the mask data
    glyph.getLayer("FontLab Mask")
    #flip it so we draw on a clean layer
    glyph.flipLayers("FontLab Mask", "foreground")
    portFLmaskData(glyph)
    #flip back we’re done
    glyph.flipLayers("FontLab Mask", "foreground")


print "Done" 
