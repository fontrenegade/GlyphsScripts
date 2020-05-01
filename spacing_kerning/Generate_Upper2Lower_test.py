#MenuTitle: Generate UC2LC test
# -*- coding: utf-8 -*-

allUpper = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
allLower = ["a","b","c","d","e","f","g","h","i", "idotless","j","jdotless","k","l","lslash","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

finalString = ""

for thisGlyph in allUpper:
  for thatGlyph in allLower:
  	finalString += "/"+thisGlyph+"/"+thatGlyph+" "

  finalString += "\n"

font.newTab (finalString)
