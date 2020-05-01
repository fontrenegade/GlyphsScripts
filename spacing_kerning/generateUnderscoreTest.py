#MenuTitle: Generate Underscore test
#Author: Jan Charvat
#Version: 1.00

__doc__ = """
Generate Underscore test for whole font
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

testString = ""
font = Glyphs.font

for thisGlyph in font.glyphs:
	if thisGlyph.name not in excludedGlyphs:
#		print thisGlyph.name, thisParenTouple
# 		print "/" +font.glyphs[thisParenTouple[0]].name+ "/" + thisGlyph.name + "/" +font.glyphs[thisParenTouple[1]].name
		testString += "/" + thisGlyph.name + "/underscore/" +thisGlyph.name + "/space"
		

font.newTab(testString)