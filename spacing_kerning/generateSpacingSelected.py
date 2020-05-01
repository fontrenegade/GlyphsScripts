#MenuTitle: Generate Spacing test For Selected
#Author: Jan Charvat
#Version: 1.00

__doc__ = """
Generate Spacing test For Selected
"""


HString = ""
OString = ""
lcGlyph = "n"
ucGlyph = "H"
counter = 0
limit = 5

font = Glyphs.font
print font.selectedLayers
for thisLayer in font.selectedLayers:
	if counter > limit:
		HString += "\n"
		counter = 0
	if thisLayer.parent.subCategory == "Lowercase":
		HString += "/" +lcGlyph + "/" + thisLayer.parent.name + "/" +lcGlyph
	else:
		HString += "/" +ucGlyph + "/" + thisLayer.parent.name + "/" +ucGlyph

	counter += 1
		
print HString
OString = HString.replace ("H", "O").replace("n", "o")


font.newTab(HString+"\n\n"+OString)