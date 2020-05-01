#MenuTitle: Generate UCLC test for selected
# -*- coding: utf-8 -*-

font = Glyphs.font
selectedGlyphs = [x.parent.name for x in font.selectedLayers]
allTest = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

finalString = ""

if len(selectedGlyphs):
    for thisGlyph in allTest:
      for thatGlyph in selectedGlyphs:
      	finalString += "/"+thisGlyph+"/"+thatGlyph+"/"+thisGlyph+" "

      finalString += "\n"

    font.newTab (finalString)
