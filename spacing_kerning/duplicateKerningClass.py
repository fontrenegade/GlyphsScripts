# MenuTitle: Duplicate Kerning Class
# autor: Jan Charvat / Renegadefonts
# -*- coding: utf-8 -*-

__doc__="""Duplicate Kerning Class with kerning pairs"""

import vanilla

lineHeight = 25
xStep = 60

font = Glyphs.font
currentGlyph = 	font.currentTab.text[font.currentTab.textCursor]
currentLKey = font.glyphs[currentGlyph].leftKerningGroup
currentRKey = font.glyphs[currentGlyph].rightKerningGroup

print currentGlyph
# print font.kerningForPair(font.selectedFontMaster, "f", "@MMK_R_period")

def nameForID(ID):
	try:
		if ID[0] == "@": # is a group
			return ID
		else: # is a glyph
			return font.glyphForId_( ID ).name
	except Exception as e:
		raise e

class DuplicateKerningClass(object):
	"""GUI for comparing two fonts for missing glyphs"""
	def __init__(self):
		self.w = vanilla.FloatingWindow((190, 160), "Duplicate Kerning Class")

		self.w.currentLKey = vanilla.TextBox((15, 20 + lineHeight, -15, 20), currentLKey, sizeStyle='small')
		self.w.newLeft = vanilla.EditText((15, 12+2*lineHeight, 50, 20), "", sizeStyle='small')

		self.w.currentGlyph = vanilla.TextBox((15+xStep, 12, -15, 20), currentGlyph, sizeStyle='regular')

		self.w.currentRKey = vanilla.TextBox((15+xStep+40, 20 + lineHeight, -15, 20), currentRKey, sizeStyle='small')
		self.w.newRight = vanilla.EditText((15+xStep+40, 12+2*lineHeight, 50, 20), "", sizeStyle='small')

		self.w.button = vanilla.Button((-140, 12+4*lineHeight, -60, 17), "Duplicate", sizeStyle='small', callback=self.Duplicate)
		self.w.setDefaultButton( self.w.button )

		self.w.open()


	def Duplicate(self, sender):
		selectedLayers = font.selectedLayers

		if (self.w.newLeft.get() != ""):
			self.DuplicateKerningPairs (currentLKey, self.w.newLeft.get(), 1)

		if (self.w.newRight.get() != ""):
			self.DuplicateKerningPairs (currentRKey, self.w.newRight.get(), 0)

		self.w.close()

	def DuplicateKerningPairs(self, oldClass, newClass, side):

		if side == 0:
			newClassLName = "@MMK_L_"+newClass
			oldClassLName = "@MMK_L_"+oldClass
			print newClassLName, oldClassLName

		if side == 1:
			newClassRName = "@MMK_R_"+newClass
			oldClassRName = "@MMK_R_"+oldClass
			print newClassRName, oldClassRName

		kerning2Add = []

		try:
			for thisMaster in font.kerning:
				for thisLeftKey in font.kerning[thisMaster]:
					if (side == 0 and thisLeftKey != oldClassLName):
						continue

					for thisRightKey in font.kerning[thisMaster][thisLeftKey]:
# 						print nameForID(thisLeftKey), nameForID(thisRightKey)
						if side == 0:
							try:
								value = font.kerningForPair(thisMaster, thisLeftKey, thisRightKey)
								kerning2Add.append((thisMaster, newClassLName, thisRightKey, value))
								print "L:", thisMaster, newClassLName, thisRightKey, font.kerningForPair(thisMaster, newClassLName, thisRightKey)
							except:
								print "LKerning for Pair failed:", thisMaster, nameForID(thisLeftKey), nameForID(thisRightKey)


						if side == 1 and thisRightKey == oldClassRName:
							try:
								value = font.kerningForPair(thisMaster, thisLeftKey, thisRightKey)
								kerning2Add.append((thisMaster, thisLeftKey, newClassRName, value))
					 			print "R:", thisMaster, thisLeftKey, newClassRName, font.kerningForPair(thisMaster, thisLeftKey, newClassRName)
							except:
								print "RKerning for Pair failed:", thisMaster, nameForID(thisLeftKey), nameForID(thisRightKey)
		except:
			pass

		print kerning2Add
		for (master, leftKey, rightKey, value) in kerning2Add:
			font.setKerningForPair (master, leftKey, rightKey, value)
			print "ADD:", master, leftKey, rightKey, value


Glyphs.clearLog()
Glyphs.font.disableUpdateInterface()

DuplicateKerningClass()

Glyphs.font.enableUpdateInterface()
Glyphs.showMacroWindow()
