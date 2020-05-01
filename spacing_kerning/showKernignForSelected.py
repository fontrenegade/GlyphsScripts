#MenuTitle: Show pairs for selected glyphs
# -*- coding: utf-8 -*-
__doc__="""Show pairs for selected glyphs in this master"""

import os.path
font = Glyphs.font
selectedMaster = font.selectedFontMaster.id # active master

pairsL = []
pairsR = []
allPairs = ""


def nameForID(ID):
	try:
		if ID[0] == "@": # is a group
			return ID[7:]
		else: # is a glyph
			if font.glyphForId_( ID ):
				return font.glyphForId_( ID ).name
	except Exception as e:
		raise e

selectedGlyphs =  [thisLayer.parent.name for thisLayer in font.selectedLayers]
print selectedGlyphs

for thisMaster in font.kerning:
	if thisMaster == selectedMaster:
		for thisLeftPair in font.kerning[thisMaster]:
			for thisRightPair in font.kerning[thisMaster][thisLeftPair]:
				rightName = nameForID(thisRightPair)
				leftName = nameForID(thisLeftPair)
				if rightName in selectedGlyphs:
					pairsR.append ((leftName,rightName))
				if leftName in selectedGlyphs:
					pairsL.append ((leftName,rightName))

print "--++LEFT SIDE:"
for thisPair in pairsR:
	print thisPair[0],thisPair[1]
	allPairs += "/"+thisPair[0]+"/"+thisPair[1]+" "

allPairs += "\n\n"

print "--++RIGHT SIDE:"
for thisPair in pairsL:
	print thisPair[0],thisPair[1]
	allPairs += "/"+thisPair[0]+"/"+thisPair[1]+" "

print allPairs
font.newTab(allPairs)


font.enableUpdateInterface()
