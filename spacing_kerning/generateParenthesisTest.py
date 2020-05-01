#MenuTitle: Generate Parenthesis test
#Author: Jan Charvat
#Version: 1.00

__doc__ = """
Generate Parenthesis test for whole font
"""

excludedGlyphs = ["commaaccentcomb",
"acute",
"breve",
"caron",
"cedilla",
"circumflex",
"dieresis",
"dotaccent",
"grave",
"hungarumlaut",
"macron",
"ogonek",
"ring",
"tilde",
"grave.case"]

parentArr = [("parenleft","parenright"),("bracketleft","bracketright"),("braceleft","braceright"),("less","greater"),("guilsinglleft","guilsinglright")]
testString = ""
font = Glyphs.font

for thisParenTouple in parentArr:
	for thisGlyph in font.glyphs:
		if thisGlyph.name not in excludedGlyphs and thisParenTouple[0] in font.glyphs:
			# print thisGlyph.name, thisParenTouple
 		# 	print "/" +font.glyphs[thisParenTouple[0]].name+ "/" + thisGlyph.name + "/" +font.glyphs[thisParenTouple[1]].name
			testString += "/" +font.glyphs[thisParenTouple[0]].name+ "/" + thisGlyph.name + "/" +font.glyphs[thisParenTouple[1]].name+"/space"
		

font.newTab(testString)