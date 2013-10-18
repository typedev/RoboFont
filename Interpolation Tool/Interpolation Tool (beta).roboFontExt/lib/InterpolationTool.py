# -*- coding: utf-8 -*-
"""
RoboFont Script
InterpolationTool.py

Created by Alexander Lubovenko on 2013-08-26.
http://github.com/typedev
"""
from __future__ import division

import sys
from math import *
from vanilla import *
from mojo.UI import *
from mojo.glyphPreview import GlyphPreview
from mojo.events import addObserver, removeObserver
from mojo.roboFont import OpenWindow
from defconAppKit.windows.baseWindow import BaseWindowController
from defconAppKit.controls.glyphLineView import GlyphLineView
from mojo import events
from mojo.drawingTools import *
from mojo.canvas import Canvas



minStem = 1
maxStem = 10

intLucas = 0
intImpallari = 1
intLinear = 2


viewFull = 0
viewShort = 1

#===================================================================================
redMark = (1,0,0,1)
greyMark = (.2, .2, .2, .5)

previewOptions = {'Inverse': False, 'xHeight Cut': False, 'Show Kerning': True, 
  					'Left to Right': True, 'Show Metrics': False, 'Show Space Matrix': True, 
 					'Upside Down': False, 'Right to Left': False, 'Stroke': False, 'Beam': False, 
					'Water Fall': False, 'Multi Line': True, 'Single Line': False, 
					'Show Control glyphs': False, 'Fill': True }

DDlist = {  'DDzero' : 0, 'DDone' : 1, 
			'DDtwo' : 2, 'DDthree' : 3, 
			'DDfour' : 4, 'DDfive' : 5, 
			'DDsix' : 6, 'DDseven' : 7, 
			'DDeight' : 8, 'DDnine' : 9  }

DDfontPath = sys.path[0] + '/tempfont.ufo'
listfonts = AllFonts()


def getListOfOpenFonts():
	lfonts = []
	for n in listfonts:
		fontFamilyName = '<empty font info>'
		fontStyleName = '<empty font info>'
		if n.info.familyName != None:
			fontFamilyName = n.info.familyName
		if n.info.styleName != None:
			fontStyleName = n.info.styleName
		lfonts.append(fontFamilyName + '/' + fontStyleName)
	lfonts.sort()
	return lfonts
		
def getGlyphNameString(number):
	st = []
	if number[0] != '-':
		for a in number:
			for n , d in DDlist.items():
				if d == int(a): 
					st.append(n)
	else:
		st.append('DDminus')
		for a in number[1:]:
			for n , d in DDlist.items():
				if d == int(a): 
					st.append(n)
	return st

def getLucasFactor(a,b,n):
	d = (log(b) - log(a))/(n+1)
	factor = []
	for i in range(n+2):
		dd = exp(log(a)+i*d)
		factor = factor + [round((dd-a)/(b-a),3)]
	return factor

	
def getLinearFactor(a,b,n):
	factor = []
	c = float((b-(a-1)))/(n+1)
	for i in range(n+2):
		factor = factor + [round(((a-1)+c*i)/10,3)]
	return factor

def getImpallariFactor(min, max, n):
	es = getLinearFactor(min, max, n)
	ls = getLucasFactor(min, max, n)
	return [ round(l*(1-i/(n+1)) + e*(i/(n+1)),3) for (i, e, l) in zip(range(n+2), es, ls)]

	
def decomposeGlyph(glyph):
	if glyph.components != None:
		for c in glyph.components:
			c.decompose()
	return glyph

def interpolateFonts(factor, minFont, maxFont, kerning = False):
	pass
	
#===================================================================================
class InterpolationWindow(BaseWindowController):
	def __init__(self, font):
		
		self.interpolatingSteps = 5
		self.pointSize = 150
		self.viewMode = viewFull
		self.resizeInProgress = False

		self.w = FloatingWindow((1000, 450), minSize=(400, 150),title = 'Interpolation Tool')

		# Upper panel

		self.w.p1 = Group((0, 0, -0, 100))
		self.w.p1.lblMethod = TextBox((10, 23, 70, 17), 'Method')
		self.w.p1.radioSelectMethod = RadioGroup((70, 3, 160, 60),
		                                 ["Luc(as) de Groot", "Pablo Impallari","Linear"],
		                                 		sizeStyle = 'small',
												callback=self.radioSelectMethodCallback)
		self.w.p1.radioSelectMethod.set(0)
		self.w.p1.vline = VerticalLine((210, 6, 1, 53))

		self.w.p1.hline = HorizontalLine((10, 65, -10, 1))	
		self.w.p1.lblAxis0001 = TextBox((230, 12, 100, 17), "Axis 00/01")

		self.w.p1.lblMinFont = TextBox((10, 75, 60, 17), "Axis 00")
		self.w.p1.cbMinFont = ComboBox((70, 72, 200, 21),
											getListOfOpenFonts(),
											callback=self.cbSelectFontCallback)
		self.w.p1.lblMaxFont = TextBox((-270, 75, 60, 17), "Axis 01")
		self.w.p1.cbMaxFont = ComboBox((-210, 72, 200, 21),
											getListOfOpenFonts(),
											callback=self.cbSelectFontCallback)
		self.w.p1.btnAddLowExtra = Button((280, 73, 100, 20), "- 100 Extra", #48
										callback=self.btnAddLowExtraCallback)
		self.w.p1.btnAddHighExtra = Button((-380, 73, 100, 20), "+ 500 Extra", #48
										callback=self.btnAddHighExtraCallback)

		self.w.p1.btnAddStep = Button((230, 35, 60, 20), "+ step", #48
										callback=self.btnAddStepCallback)
		self.w.p1.btnDelStep = Button((300, 35, 60, 20), "- step",
										callback=self.btnDelStepCallback)
		self.w.p1.vline2 = VerticalLine((380, 6, 1, 53))

		# Glyphs lineview

		self.w.lineView = MultiLineView((0, 100, -0, -80), 
												pointSize=self.pointSize, 
												lineHeight = self.pointSize*1.75,
												bordered = True,
												hasVerticalScroller = True,
												# displayOptions = dict(previewOptions),
												selectionCallback=self.lineViewSelectionCallback,
												doubleClickCallbak=self.lineViewDoubleSelectionCallback )

		self.w.lblStatus = TextBox((15, -105, -20, 17), 'Status bar')
		self.w.lineView.setFont(font)

		# View panel 

		self.w.pV = Group((-270, 12, 250, 100))
		segments = [{'width':40, 'title':'Full'},{'width':40, 'title':'Short'}]
		yPosV = 10
		xPosV = 0
		self.w.pV.btnPreviwGlyphSmall = Button((0,yPosV+3,65,14),'Preview...',
										sizeStyle='mini',
										callback=self.btnPreviwButtonCallback)
		self.w.pV.btnSwitchViewMode = SegmentedButton ((70, yPosV, 90, 20), 
										segmentDescriptions = segments,
										selectionStyle='one', sizeStyle='mini', #48
										callback=self.btnSwitchViewMode)
		self.w.pV.btnSwitchViewMode.set(0)
		self.w.pV.lblGlyphBtnHint = TextBox((15, 0, 100, 12), "Glyph", sizeStyle='mini')

		self.w.pV.lblViewMode = TextBox((85, 0, 100, 12), "View mode", sizeStyle='mini')
		self.w.pV.lblPointSize = TextBox((175, 0, 100, 12), "Preview size", sizeStyle='mini')
		self.w.pV.sliderPointSize = Slider((165, yPosV+3, 80, 17), 
												stopOnTickMarks=False,
												callback=self.sliderPointSizeCallback,
												sizeStyle = 'mini')
		self.w.pV.sliderPointSize.enable(True)
		self.w.pV.sliderPointSize.setMinValue(72)
		self.w.pV.sliderPointSize.setMaxValue(512)
		self.w.pV.sliderPointSize.set(self.pointSize)
		self.w.pV.lblGlyphBtnHint.show(False)
		self.w.pV.btnPreviwGlyphSmall.show(False)

		# Bottom panel

		self.w.p2 = Group((0, -80, -0, -0))
		self.w.p2.lblTuner0001 = TextBox((10, -68, 100, 17), "Tuner 00/01")
		self.w.p2.sliderFactor = Slider((110, -65, 210, 23), 
												tickMarkCount=2, 
												stopOnTickMarks=False,
												callback=self.sliderFactorCallback)
		self.w.p2.sliderFactor.enable(False)
		self.w.p2.sliderFactor.setMinValue(0)
		self.w.p2.sliderFactor.setMaxValue(1000)
		self.w.p2.sliderFactor.set(500)
		self.w.p2.lblMin = TextBox((110, -38, 70, 17), '0', alignment='left')
		self.w.p2.lblMax = TextBox((250, -38, 70, 17), '1000', alignment='right')
		self.w.p2.lblCurrent = TextBox((185, -38, 60, 17), '500', alignment='center')
		self.w.p2.lblMin.show(False)
		self.w.p2.lblMax.show(False)
		self.w.p2.lblCurrent.show(False)

		self.w.p2.vline3 = VerticalLine((340, -73, 1, -10))

		self.w.p2.btnPreviwGlyph = Button((360, -70, 130, 20), "Preview glyph...",
		 								callback=self.btnPreviwButtonCallback)
		self.w.p2.btnDeleteInstance = Button((360, -40, 130, 20), "Delete Instance",
		 								callback=self.btnDeleteInstanceCallback)
		self.w.p2.spinner = ProgressSpinner((503, 20, 32, 32),
                                        displayWhenStopped=False)
		self.w.p2.btnGenerateSeleced = Button((-220, -70, -10, 20), "Generate Selected Instance...",
		 								callback=self.btnGenerateSelectedCallback)
		self.w.p2.btnGenerateAll = Button((-220, -40, -10, 20), "Generate All Instances...",
		 								callback=self.btnGenerateSelectedCallback)
		self.w.p2.btnGenerateSeleced.enable(False)
		self.w.p2.btnGenerateAll.enable(False)

		# Init section

		self.minFont = None 
		self.minFontName = []
		self.maxFont = None 
		self.minFontName = []
		self.DDfont = OpenFont(DDfontPath,showUI = False)

		self.indexSelectedGlyph = None
		self.interpolateMethod = intLucas
		self.setInterpolateScale()
		self.drawGlyphsLine(dict(glyph=None))

		self.w.bind('resize', self.windowResize)
		events.addObserver(self, "drawMessagePreviewOnly", 'draw')
		events.addObserver(self, "drawGlyphsLine", "currentGlyphChanged")
		events.addObserver(self, "drawGlyphsLine", "draw")

		self.setUpBaseWindowBehavior()
		self.w.open()

	def changeViewMode(self):
		wS = self.w.getPosSize()
		lS = self.w.lineView.getPosSize()
		self.resizeInProgress = True
		if self.viewMode == viewShort:
			self.w.pV.setPosSize((-270, 2, 250, 100))
			self.w.p1.show(False)
			self.w.pV.lblGlyphBtnHint.show(True)
			self.w.pV.btnPreviwGlyphSmall.show(True)
			self.w.lineView.setPosSize((0,0,-0,-0))
			self.w.p2.show(False)
			hW = wS[3] + lS[3] - lS[1]
			self.w.resize( wS[2], hW )
		else:
			self.w.pV.setPosSize((-270, 12, 250, 100))
			self.w.p1.show(True)
			self.w.p2.show(True)
			self.w.pV.lblGlyphBtnHint.show(False)
			self.w.pV.btnPreviwGlyphSmall.show(False)
			if wS[2] < 770: 
				hW = 770
			else:
				hW = wS[2]
			self.w.resize(hW, wS[3] + 180 )
			self.w.lineView.setPosSize((0, 100, -0, -80))
		self.resizeInProgress = False

	def btnSwitchViewMode(self, sender):
		if sender.get() != self.viewMode:
			self.viewMode = sender.get()
			self.changeViewMode()

	def windowResize(self, sender):
		wS = self.w.getPosSize()
		if (wS[3] < 313) or (wS[2] < 770):
			if not self.resizeInProgress:
				self.viewMode = viewShort
				self.w.pV.btnSwitchViewMode.set(1)
				self.changeViewMode()

	def windowCloseCallback(self, sender):
		events.removeObserver(self, "draw")
		events.removeObserver(self, "currentGlyphChanged")
		super(InterpolationWindow, self).windowCloseCallback(sender)

	def drawMessagePreviewOnly(self, info):
		glyph = info["glyph"]
		if self.minFont.has_key(glyph.name) and self.maxFont.has_key(glyph.name): pass
		else:
			r = 0
			g = 0
			b = 0
			a = .5
			font("Menlo", 20)
			stroke(None)
			fill(r, g, b, a)
			text('Preview ONLY. Any changes will be lost.', (20, -40))
	
	def sliderPointSizeCallback(self, sender):
		self.pointSize = sender.get()
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))
	
	def btnAddLowExtraCallback(self, sender):
		minf = self.interpolateScale[0]
		self.interpolateScale.insert(0, minf - .1)
		self.indexSelectedGlyph = None
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))

	def btnAddHighExtraCallback(self, sender):
		maxf = self.interpolateScale[-1]
		self.interpolateScale.append(maxf + .5)
		self.indexSelectedGlyph = None
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))

	def btnDeleteInstanceCallback(self, sender):
		self.interpolateScale.pop(self.indexSelectedGlyph)
		self.indexSelectedGlyph = None
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))
		
	def sliderFactorCallback(self, sender):
		if self.indexSelectedGlyph != None:
			factor = round(float(sender.get())/1000,3)
			# if factor != 1000:
			self.interpolateScale[self.indexSelectedGlyph] = factor
			# else:
				# self.interpolateScale[self.indexSelectedGlyph] = factor + 1
			self.w.p2.lblCurrent.set(str(int(factor*1000)))
			self.drawGlyphsLine(dict(glyph=CurrentGlyph()))

	def blockSlider(self, showFactor = 0):
		self.w.p2.lblMin.set(0)
		self.w.p2.lblMax.set(10)
		self.w.p2.sliderFactor.set(5)
		self.w.p2.lblMin.show(False)
		self.w.p2.lblMax.show(False)
		self.w.p2.sliderFactor.enable(False)
		self.w.p2.lblCurrent.show(True)
		self.w.p2.lblCurrent.set(str(showFactor))

	def openSelectedGlyph(self):
		cg = CurrentGlyph()
		minFamily, minStyle = self.minFontName
		maxFamily, maxStyle = self.maxFontName
		lineGlyphs = self.w.lineView.get()
		selectedname = lineGlyphs[self.indexSelectedGlyph].name
		if selectedname != '0' and selectedname != '1000':
			tempname = cg.name+'.'+ selectedname +'.Preview.'
			self.DDfont.newGlyph( tempname, clear = True)
			self.DDfont[tempname] = self.DDfont[selectedname].copy()
			for c in self.DDfont[tempname].components:
				self.DDfont[tempname].removeComponent(c)
			self.DDfont.round()
			OpenGlyphWindow(self.DDfont[tempname])
		elif selectedname == '0':
			OpenGlyphWindow(listfonts.getFontsByFamilyNameStyleName( minFamily, minStyle ) [cg.name])
		elif selectedname == '1000':
			OpenGlyphWindow(listfonts.getFontsByFamilyNameStyleName( maxFamily, maxStyle ) [cg.name])
		
	def btnPreviwButtonCallback(self, sender):
		self.openSelectedGlyph()

	def radioSelectMethodCallback(self, sender):
		self.interpolateMethod = sender.get()
		self.setInterpolateScale()
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))
		
	def btnAddStepCallback(self, sender):
		self.interpolatingSteps = self.interpolatingSteps +1
		self.setInterpolateScale()
		self.indexSelectedGlyph = None
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))
		
	def btnDelStepCallback(self, sender):
		if self.interpolatingSteps != 1:
			self.interpolatingSteps = self.interpolatingSteps -1
		self.indexSelectedGlyph = None
		self.setInterpolateScale()
		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))

	def btnGenerateSelectedCallback(self,sender):
		pass


	def btnGenerateAllCallback(self,sender):
		pass

	def cbSelectFontCallback(self, sender):
		self.w.p2.spinner.start()
		lfonts = getListOfOpenFonts()
		if sender.get() in lfonts:
			l2 = []
			l1 = sender.get()
			l2 = l1.split('/')
			if sender == self.w.p1.cbMinFont:
				self.minFontName = l2
				self.minFont = listfonts.getFontsByFamilyNameStyleName(l2[0],l2[1]).copy() 
			if sender == self.w.p1.cbMaxFont:
				self.maxFontName = l2
				self.maxFont = listfonts.getFontsByFamilyNameStyleName(l2[0],l2[1]).copy()
			self.drawGlyphsLine(dict(glyph=CurrentGlyph()))
		self.w.p2.spinner.stop()

	def lineViewDoubleSelectionCallback(self, sender): 
		self.openSelectedGlyph()

	def lineViewSelectionCallback(self, sender): 		
		lineGlyphs = self.w.lineView.get()
		selGlyph = self.w.lineView.getSelectedGlyph()
		# self.nameOfSelectedGlyph = selGlyph.name
		if selGlyph != None:
			i = 0
			for g in lineGlyphs:
				if selGlyph.name == g.name:
					self.indexSelectedGlyph = i
					break
				i = i+1

			factor = int(selGlyph.name)
			if (factor != 0) and (factor != 1000):
				self.w.p2.sliderFactor.enable(True)

				if factor > 1000:
					minf = int(lineGlyphs[self.indexSelectedGlyph-1].name)+10
				else:
					minf = int(lineGlyphs[self.indexSelectedGlyph-1].name)+1

				if factor < 1000:
					maxf = int(lineGlyphs[self.indexSelectedGlyph+1].name)-1
				else:
					if factor == int(lineGlyphs[-1].name): 
						maxf = factor + 500
					else:
						maxf = int(lineGlyphs[self.indexSelectedGlyph+1].name)-1

				if factor < 0:
					maxf = int(lineGlyphs[self.indexSelectedGlyph+1].name)-1
					if factor == int(lineGlyphs[0].name): 
						minf = factor - 100
					else:
						minf = int(lineGlyphs[self.indexSelectedGlyph-1].name)+1

				self.w.p2.sliderFactor.setMaxValue(maxf)
				self.w.p2.lblMax.set(str(maxf))
				self.w.p2.lblMax.show(True)
				
				self.w.p2.sliderFactor.setMinValue(minf)
				self.w.p2.lblMin.show(True)
				self.w.p2.lblMin.set(str(minf))
				
				self.w.p2.sliderFactor.set(factor)
				self.w.p2.lblCurrent.set(str(factor))
				self.w.p2.lblCurrent.show(True)
				self.w.pV.btnPreviwGlyphSmall.setTitle('Preview...')
				self.w.p2.btnPreviwGlyph.setTitle('Preview glyph...')
			else: 
				self.w.p2.btnPreviwGlyph.setTitle('Edit glyph...')
				self.w.pV.btnPreviwGlyphSmall.setTitle('Edit...')
				self.blockSlider(factor)

		self.drawGlyphsLine(dict(glyph=CurrentGlyph()))


	def setInterpolateScale(self):
		if self.interpolateMethod == intLucas:
			self.interpolateScale = getLucasFactor( minStem, maxStem, self.interpolatingSteps )
		if self.interpolateMethod == intImpallari:
			self.interpolateScale = getImpallariFactor( minStem, maxStem, self.interpolatingSteps )
		if self.interpolateMethod == intLinear:
			self.interpolateScale = getLinearFactor( minStem, maxStem, self.interpolatingSteps )
			
	def drawGlyphsLine(self, info):
		self.w.lblStatus.set('') 		
		if (self.minFont != None) and (self.maxFont != None): 

			if self.indexSelectedGlyph == None:
				self.blockSlider()

			# glyph = None
			# if self.minFont.has_key(CurrentGlyph().name) and self.maxFont.has_key(CurrentGlyph().name):
			glyph = CurrentGlyph()
			glyphs = []

			if glyph is not None:
				glyphName = glyph.name
				idx = 0
				if self.minFont.has_key(glyphName) and self.maxFont.has_key(glyphName):
					minFamily, minStyle = self.minFontName
					maxFamily, maxStyle = self.maxFontName
					# tgmin = listfonts.getFontsByFamilyNameStyleName( minFamily, minStyle )[glyphName]
					# tgmax = listfonts.getFontsByFamilyNameStyleName( maxFamily, maxStyle )[glyphName]
					# self.minFont.insertGlyph( listfonts.getFontsByFamilyNameStyleName( minFamily, minStyle ) [glyphName] )
					# self.maxFont.insertGlyph( listfonts.getFontsByFamilyNameStyleName( maxFamily, maxStyle ) [glyphName] )
					self.minFont.removeGlyph(glyphName)
					self.maxFont.removeGlyph(glyphName)
					self.minFont.insertGlyph( listfonts.getFontsByFamilyNameStyleName( minFamily, minStyle )[glyphName], name = glyphName )
					self.maxFont.insertGlyph( listfonts.getFontsByFamilyNameStyleName( maxFamily, maxStyle )[glyphName], name = glyphName )
				sg = decomposeGlyph(self.minFont[glyphName])
				dg = decomposeGlyph(self.maxFont[glyphName])


				for i in self.interpolateScale:
					gname = str(int(i*1000))
					g = self.DDfont.newGlyph(gname , clear = True)

					isComp = sg.isCompatible(dg,True)
					if isComp[0]:
						g.interpolate(i,sg,dg)
						stname = getGlyphNameString(gname)
						ddXpos = 0
						ddYpos = -310
						if idx == self.indexSelectedGlyph:
							g.appendComponent('DDbracketleft', (ddXpos, ddYpos + 4 ), (.08,.08))
							ddXpos = ddXpos + 70

						for a in stname:
							g.appendComponent(a, (ddXpos, ddYpos), (.08,.08))
							ddXpos = ddXpos + 70

						if idx == self.indexSelectedGlyph:
							g.appendComponent('DDbracketright', (ddXpos, ddYpos + 4 ), (.08,.08))

						idx = idx + 1
						g.update()
						glyphs.append(g)
					else:
						self.w.lblStatus.set(isComp[1][0])

			# self.w.lineView.setDisplayStates(previewOptions)
			self.w.lineView.setPointSize(self.pointSize)	
			self.w.lineView.set(glyphs)

InterpolationWindow(CurrentFont())
	
