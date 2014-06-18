from robofab.world import CurrentFont
from mojo.roboFont import *



        


import sys
from vanilla import *
from mojo.UI import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo import events


redMark = (1,0,0,1)
greyMark = (.2, .2, .2, .5)

lfonts = []
listfonts = AllFonts()

for n in listfonts:
    lfonts.append(n.info.familyName+'/'+n.info.styleName)

class CheckInterpolationWindow(BaseWindowController):
    def __init__(self):

        self.fontA = None
        self.fontB = None

        self.w = FloatingWindow((430, 100), title = 'Copy Metrics Tool')
        self.w.cbFontA = ComboBox((10, 10, 200, 21),
                                            lfonts,
                                            callback=self.cbFontACallback)
        self.w.cbFontB = ComboBox((220, 10, 200, 21),
                                            lfonts,
                                            callback=self.cbFontBCallback)
        self.w.btnCheck = Button((320, 45, 100, 20), "Copy", #48
                                        callback=self.btnCheckCallback)
        self.w.spinner = ProgressSpinner((290, 48, 16, 16),
                                        displayWhenStopped=False)

        self.w.open()

    def cbFontACallback(self, sender):
        if sender.get() in lfonts:
            l2 = []
            l1 = sender.get()
            l2 = l1.split('/')
            self.fontA = listfonts.getFontsByFamilyNameStyleName(l2[0],l2[1]) 
        
    def cbFontBCallback(self, sender):
        if sender.get() in lfonts:
            l2 = []
            l1 = sender.get()
            l2 = l1.split('/')
            self.fontB = listfonts.getFontsByFamilyNameStyleName(l2[0],l2[1])


        
    def btnCheckCallback(self, sender):
        if (self.fontA != None) and (self.fontB != None):
            self.w.spinner.start()
            dfontChanged = False

            for gd in self.fontB:
                if gd.name in self.fontA.keys():
                    gs = self.fontA[gd.name]
                
                    
                    if gd.leftMargin != gs.leftMargin:
                        gd.leftMargin = gs.leftMargin
                        print gd.name + ' LM equal ' + gs.name
                        gd.update()
                        dfontChanged = True
                        
                    if gd.rightMargin != gs.rightMargin:
                        gd.rightMargin = gs.rightMargin
                        print gd.name + ' RM equal ' + gs.name
                        gd.update()
                        dfontChanged = True
                        
                    
            if dfontChanged:
                self.fontB.update()
                print 'Font updated'
            else:
                print 'Fonts are equal'
            
            print 'Done.'
            self.w.spinner.stop()
            
CheckInterpolationWindow()