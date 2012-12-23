# RoboFont Script
# Just one click to show all ready glyphs in SpaceCenter
# Alexander Lubovenko
# http://github.com/typedev

from mojo.UI import *

font = CurrentFont()

a=[]
for i in font:
    if i:
       a.append(i.name) 

OpenSpaceCenter(font)
SC = CurrentSpaceCenter()
SC.set(a)
