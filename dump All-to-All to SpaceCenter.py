# RoboFont Script
# Generate dump text from the selected glyphs to SpaceCenter
# Alexander Lubovenko
# http://github.com/typedev

from robofab.world import CurrentFont
from mojo.UI import *

font = CurrentFont()

listglyphs = font.selection

result = []

for b in listglyphs:
	for i in listglyphs:
		result.append(i)
		result.append(b)
		
OpenSpaceCenter(font)
SC = CurrentSpaceCenter()
SC.set(result)

