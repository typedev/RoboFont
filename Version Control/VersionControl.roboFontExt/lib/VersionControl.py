# RoboFont Script
# Version Control 
# Alexander Lubovenko
# http://github.com/typedev

from mojo.UI import *
from vanilla import *
from mojo.glyphPreview import GlyphPreview
from mojo.events import addObserver, removeObserver
from mojo.roboFont import OpenWindow
from time import asctime


libVC = 'com.typedev.version_control.'
font = CurrentFont()

def getVersionNumber(glyphName):
	libKey = libVC + glyphName
	if font.lib.has_key(libKey): 
		font.lib[libKey] = font.lib[libKey] + 1
	else:
		font.lib[libKey] = 1
	return font.lib[libKey]


def setVersionNumber(glyphName, versionNumber = 0):
	libKey = libVC + glyphName
	font.lib[libKey] = versionNumber


def checkVersionNumbers():
	gversions = []
	for g in font:
		if '.ver.' not in g.name:
			gversions = GetListVersions(g.name)
			if gversions != []:
				gname = gversions[-1]
				a = gname.split('.')
				lastnumber = int(a[-1]) 
				setVersionNumber( g.name, lastnumber )
			else:
				setVersionNumber( g.name )


def cloneGlyph(glyph,name=''):
	if name == '':
		oldname = glyph.name
	else:
		oldname = name
	i = getVersionNumber(oldname)
	newName = oldname+'.ver.'+'%03d' % i
	font.insertGlyph(glyph,newName)
	font.update()
	font[newName].note = 'Version created ' + asctime()
	font[newName].update()
	font.update()

def GetListVersions(glyphName):
	gversions = []
	if '.ver.' in glyphName:
		selname = glyphName.split('.')
		if 'ver' == selname[-2]:
			selname.pop()
			selname.pop()
			glyphName='.'.join(selname)
			gversions.append(glyphName)
	for g in font:
		if (glyphName + '.ver.') in g.name:
			gversions.append(g.name)
	gversions.sort()
	return gversions


class VersionControl:

	def __init__(self):

		self.w = FloatingWindow((250, 530),minSize=(200, 400),title = 'Version Control')

		self.PreviewPanel = Group((0, 0, -0, -0))
		self.PreviewPanel.Preview = GlyphPreview((0, 0, -15, 0))
		self.PreviewPanel.GlyphInfo = TextBox((5, -13, 0, 12), '', alignment='left', selectable=False, sizeStyle='mini')
		self.PreviewPanel.hline = HorizontalLine((5, -1, -5, 1))
		self.Control = Group((0, 0, -0, -0))

		self.Control.VersionsList = List((0, 30, -0, -0), [], allowsMultipleSelection = False,
																selectionCallback=self.selectionVersionCallback,
																doubleClickCallback=self.selectionDoubleVersionCallback)

		self.Control.btnAdd = Button((5,5,30,20), '+', callback=self.btnAddCallback)
		self.Control.btnDel = Button((40,5,30,20), '-', callback=self.btnDelCallback)
		self.Control.btnSwap = Button((75,5,40,20), '<>', callback=self.btnSwapCallback)
		self.Control.btnShow = Button((120,5,40,20), 'Sc', callback=self.btnShowCallback)

		self.Note = TextEditor((5, 5, -5, -5))

		descriptions = [
						dict(label="Preview", view=self.PreviewPanel, size=320, collapsed=False, canResize=True),
						dict(label="Control", view=self.Control, minSize=100, size=140, collapsed=False, canResize=True),
						dict(label="Note", view=self.Note, minSize=100, size=140, collapsed=True, canResize=True),
						]



		addObserver(self, "_currentGlyphChanged", "currentGlyphChanged")
		self.w.bind("close", self.windowClose)
		self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions )
		checkVersionNumbers()
		self.updateVersionsList()
		self.w.open()

	def selectionVersionCallback(self, sender):
		idx = sender.getSelection()
		if idx != []:
			self.setGlyph( font[ self.Control.VersionsList[ idx[0] ] ] )

	def selectionDoubleVersionCallback(self, sender):
		idx = sender.getSelection()
		if idx != []:
			name = self.Control.VersionsList[idx [0]]
			SetCurrentGlyphByName(name)
			self.setGlyph( font[ name ] )
			OpenGlyphWindow( font[ name ] )
		
	def updateVersionsList(self):
		if CurrentGlyph() != None:
			self.setGlyph(CurrentGlyph())
			self.Control.VersionsList.set([])
			self.Control.VersionsList.set( GetListVersions( CurrentGlyph().name ) )
			if CurrentGlyph().name in self.Control.VersionsList:
				self.Control.VersionsList.setSelection([ self.Control.VersionsList.index(CurrentGlyph().name) ])

	def _currentGlyphChanged(self, info):
		self.updateVersionsList()

	def btnAddCallback(self, sender):
		glyph = CurrentGlyph()
		if '.ver.' in glyph.name:
			lname = glyph.name.split('.')
			if 'ver' == lname[-2]:
				lname.pop()
				lname.pop()
				sname='.'.join(lname)
				cloneGlyph(glyph,sname)
		else: 
			cloneGlyph(glyph)
		font.update()
		self.updateVersionsList()

	def btnDelCallback(self, sender):
		idx = self.Control.VersionsList.getSelection()
		if idx != []:
			name = self.Control.VersionsList[idx [0]]
			if '.ver.' in name:

				aa = font.lib[ 'public.glyphOrder' ]
				if name in aa:
					aa.remove(name)
					font.lib[ 'public.glyphOrder' ] = aa
				font.removeGlyph (name)
				font.update()

				self.Control.VersionsList.remove(name)
				self.updateVersionsList()

	def btnSwapCallback(self, sender):
		idx = self.Control.VersionsList.getSelection()
		if idx != []:
			vName = self.Control.VersionsList[idx [0]]
			vGlyph = font[vName]
			vUcode = font[vName].unicode

			cGlyph = CurrentGlyph()
			cName = cGlyph.name
			cUcode = cGlyph.unicode

			if (vName != cName) and ('.ver.' not in cName):
				font.removeGlyph(cName)
				font.insertGlyph(vGlyph,cName)
				font[cName].unicode = cUcode
				font[cName].update()
				font.removeGlyph(vName)
				font.insertGlyph(cGlyph,vName)
				font[vName].update()
				font.glyphOrder = font.lib['public.glyphOrder']
				font.update()
				self.updateVersionsList()
				OpenGlyphWindow( font[ cName ] )	

	def btnShowCallback(self, sender):
		cGlyph = CurrentGlyph().name
		gversions = GetListVersions(cGlyph)
		if gversions != []:
			OpenSpaceCenter(font)
			SC = CurrentSpaceCenter()
			if '.ver.' not in cGlyph:
				gversions.insert(0,cGlyph)
			SC.set(gversions)


	def setGlyph(self, glyph):
		self.PreviewPanel.GlyphInfo.set('')
		self.PreviewPanel.Preview.setGlyph(glyph)
		ucode = '-'
		if glyph.unicode != None:
			ucode = "%04X" % (glyph.unicode)
		gInfo = 'Glyph: ' + glyph.name + ' | U: '+ ucode + ' | Left: ' + str(int(round(glyph.leftMargin,0))) + ' | Right: ' + str(int(round(glyph.rightMargin)))
		self.PreviewPanel.GlyphInfo.set(gInfo)
		self.Note.set('')
		if glyph.note != None:
			self.Note.set(glyph.note)

	def windowClose(self, sender):
		removeObserver(self, "_currentGlyphChanged")

VersionControl()