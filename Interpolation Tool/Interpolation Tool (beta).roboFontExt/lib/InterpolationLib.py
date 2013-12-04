from mojo.roboFont import *
from time import asctime
from math import *
# import ReportWindow
# reload(ReportWindow)

redMark = (1,0,0,1)
greyMark = (.2, .2, .2, .5)


from vanilla import *

# InterpolationReport = ReportWindow.ReportWindow('Interpolation Report')

def mathVM(minVM,maxVM,factor):
	delta = maxVM - minVM
	return int(round(minVM+factor*delta,0))

class ProgressBarWindow(object):

	def __init__(self, Count = 0, nameOfProcess = ''):
		self.w = FloatingWindow((280, 65))
		self.w.label = TextBox((10, 12, -10, 24), nameOfProcess)
		self.w.bar = ProgressBar((10, 40, -10, 16),minValue=0, maxValue = Count)
		self.w.center()
		self.w.open()

	def increment(self):
		self.w.bar.increment()

	def closeProgress(self):
		self.w.close()


def decomposeGlyph(glyph):
	if glyph.components != None:
		for c in glyph.components:
			c.decompose()
	return glyph

def getListOfCompatibleGlyphs(bFont,dFont, mark = True):
	bGlyphCount = len(bFont)
	dGlyphCount = len(dFont)
	okGlyphs = []
	wrongGlyphs = []
	missingGlyphs = []
	Progress = ProgressBarWindow((bGlyphCount+dGlyphCount),'Checking glyphs...')
	copyBfont = bFont.copy()
	copyDfont = dFont.copy()
	for glyph in bFont:
		Progress.increment()
		if dFont.has_key( glyph.name ): 
			# print "++++++++++++++++", glyph.name
			# aGlyph = bFont[glyph.name]
			# bGlyph = dFont[glyph.name]
			aGlyph = decomposeGlyph(copyBfont[glyph.name])
			bGlyph = decomposeGlyph(copyDfont[glyph.name])
			isComp = aGlyph.isCompatible (bGlyph, True)
			if isComp[0]:
				okGlyphs.append(glyph.name)
			else:
				a = isComp[1][0]
				a = a.replace('Fatal error: ','')
				wrongGlyphs.append([glyph.name, a])
				if mark:
					glyph.mark = redMark
					dFont[ glyph.name ].mark = redMark
		else: 
			missingGlyphs.append([bFont.info.familyName, bFont.info.styleName, glyph.name])
			if mark:
				glyph.mark = greyMark
	for glyph in dFont:
		Progress.increment()

		if bFont.has_key( glyph.name ): 
			pass
		else:
			missingGlyphs.append([dFont.info.familyName, dFont.info.styleName, glyph.name])
			if mark:
				glyph.mark = greyMark
	# bFont.update()
	# dFont.update()
	Progress.closeProgress()
	return okGlyphs, wrongGlyphs, missingGlyphs

def getRightFontOrder(bFont,dFont):
	bGlyphCount = len(bFont)
	dGlyphCount = len(dFont)
	if bGlyphCount == dGlyphCount:
		return bFont, dFont
	else:
		if bGlyphCount > dGlyphCount:
			return bFont, dFont
		if bGlyphCount < dGlyphCount:
			return dFont, bFont


def checkCompatibilityConsole(bFont,dFont, mark = True, report = True):
	# InterpolationReport.addToReport( "Interpolation Tool report" )
	# InterpolationReport.addToReport( "Checking glyphs... " + asctime() )
	print "Interpolation Tool report"
	print "Checking glyphs... ", asctime()
	okGlyphs = []
	wrongGlyphs = []
	missingGlyphs = []


	aFont, bFont = getRightFontOrder(bFont,dFont)
	okGlyphs, wrongGlyphs, missingGlyphs = getListOfCompatibleGlyphs( aFont, bFont, mark )


	if report:
		Progress = ProgressBarWindow(len(wrongGlyphs)+len(missingGlyphs),'Making report...')
		for glyph in wrongGlyphs:
			gname, gerror = glyph
			print "Incompatible:", glyph[0] ,"Reason:", gerror, "Marked RED label"
			Progress.increment()

		for glyph in missingGlyphs:
			print "Missing Glyph:", glyph[0], glyph[1], glyph[2], "Marked GREY label"
			Progress.increment()
		Progress.closeProgress()

	# for glyph in wrongGlyphs:
	# 	gname, gerror = glyph
	# 	InterpolationReport.addToReport( "Incompatible: " + glyph[0] + " Reason: " + gerror + " Marked RED label." )
	# 	Progress.increment()

	# for glyph in missingGlyphs:
	# 	InterpolationReport.addToReport( "Missing Glyph: " + glyph[0] +' '+ glyph[1] +' '+ glyph[2] + " Marked GREY label." )
	# 	Progress.increment()
	return okGlyphs


def InterpolateFonts(minFont,maxFont, 
						compatibleGlyphs = [], 
						intrepolateScale = [], 
						kerning = True, 
						deletesmallpairs = True, 
						lowpair = -5, 
						highpair = 5):
	# InterpolationReport.addToReport( "Interpolate..." )
	print "Interpolate..."

	aFont, bFont = getRightFontOrder(minFont, maxFont)



	for factor in intrepolateScale:

		ffactor = int(factor * 1000)
		if (ffactor != 0) and (ffactor != 1000): 
			fontNewWeightName = str(ffactor)

			# InterpolationReport.addToReport( "Generate instance: " + fontNewWeightName + ' -- ' + asctime() )
			print "Generate instance: ", fontNewWeightName, ' -- ', asctime()

			resultFont = NewFont(aFont.info.familyName, fontNewWeightName )

			print "Dimensions:"


			A = aFont.info.ascender
			B = bFont.info.ascender
			resultFont.info.ascender = mathVM(A,B,factor)

			print '\tAscender:', resultFont.info.ascender

			A = aFont.info.capHeight
			B = bFont.info.capHeight
			resultFont.info.capHeight = mathVM(A,B,factor)	

			print '\tCap-height', resultFont.info.capHeight

			A = aFont.info.xHeight
			B = bFont.info.xHeight
			resultFont.info.xHeight = mathVM(A,B,factor)

			print '\tx-height', resultFont.info.xHeight

			A = aFont.info.descender
			B = bFont.info.descender
			resultFont.info.descender = mathVM(A,B,factor)

			print '\tDescender:', resultFont.info.descender





			# Copy groups 
			Progress = ProgressBarWindow(len(aFont.groups.items()),'['+fontNewWeightName+'] Copying groups...')
			# InterpolationReport.addToReport('Groups: ' + str(len(aFont.groups.items())) )
			print 'Groups: ', str(len(aFont.groups.items()))
			for group, value in aFont.groups.items():
				resultFont.groups[group] = value
				Progress.increment()
			Progress.closeProgress()

			# Interpolate kerning 
			if kerning:
				resultFont.kerning.interpolate(aFont.kerning, bFont.kerning, factor )
				if deletesmallpairs:
					dic = {}
					totalPairs = len(resultFont.kerning.items())
					Progress = ProgressBarWindow( totalPairs ,'['+fontNewWeightName+'] Interpolate kerning...')
					# InterpolationReport.addToReport('Interpolate kerning: ')
					# InterpolationReport.addToReport('total pairs ' + str(totalPairs) )
					# InterpolationReport.addToReport('removing pairs between -5 and 5 ' ) 
					for i in resultFont.kerning.items():
						# InterpolationReport.addToReport(str(i[1]) +' '+ str(i[0]))
						Progress.increment()
						if i[1] != 0:
							if i[1] > highpair: 
								dic[i[0]] = int(round(i[1]))
							else:
								if i[1] < lowpair: 
									dic[i[0]] = int(round(i[1]))

					resultFont.kerning.clear()    
					resultFont.kerning.update(dic)
				# InterpolationReport.addToReport('total pairs ' + str(len(resultFont.kerning.items())) ) 
					Progress.closeProgress()

			# Interpolate glyphs
			Progress = ProgressBarWindow(len(compatibleGlyphs),'['+fontNewWeightName+'] Interpolate glyphs...')

			for glyphname in compatibleGlyphs:
				newglyph = resultFont.newGlyph( glyphname )
				newglyph.interpolate (factor, aFont[ glyphname ], bFont[ glyphname ])
				newglyph.unicode = aFont[ glyphname ].unicode
				newglyph.update()
				Progress.increment()

			resultFont.round()
			
			Progress.closeProgress()


			# resultFont.glyphOrder = aFont.glyphOrder	
			# InterpolationReport.addToReport(  "Instance: " + fontNewWeightName + " done" )
			print "Instance: ", fontNewWeightName, " done"

	minFont.update()
	maxFont.update()
	# InterpolationReport.addToReport( "All done. =)" )
	# InterpolationReport.showReport()
	print "All done. =)"
