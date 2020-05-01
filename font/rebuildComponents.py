#MenuTitle: Rebuild Components
# -*- coding: utf-8 -*-
__doc__="""
Moves outlines to background, then tries to rebuild the glyph with components in the foreground. Tries to position the accents as precisely as possible.
"""

import GlyphsApp
from Foundation import NSRect
from Foundation import NSPoint
from Foundation import NSSize

Font = Glyphs.font
selectedLayers = Font.selectedLayers

errorOccured = False
accentFound = False
tempPathsToReturn = []
comparePrecision = 2

oneGlyph = True 

unrebuildableGlyphs = ["AE", "Aogonek", "Eogonek", "Iogonek", "Uogonek",  "aogonek", "eogonek", "iogonek", "uogonek", "Ccedilla", "Scedilla", "Tcedilla", "ccedilla", "scedilla", "tcedilla", "Lslash", "lslash", "Oslash", "oslash", "Dcroat", "Dcroat", "Hbar", "hbar", "Eth", "quotedblbase", "Theta", "theta", "trademark", "numero", "i", "j", "i.dot"]

changeColors = True

class errorOccuredException (Exception):
	def __init__(self):
		self.value = "error occured"
	def __str__(self):
		return "error occured"

def boundsForPaths( thesePaths ):
	thisOriginX = min( [p.bounds.origin.x for p in thesePaths] )
	thisOriginY = min( [p.bounds.origin.y for p in thesePaths] )
	thisTopRightX = max( [p.bounds.origin.x + p.bounds.size.width  for p in thesePaths] )
	thisTopRightY = max( [p.bounds.origin.y + p.bounds.size.height for p in thesePaths] )
	returnRect = NSRect()
	returnRect.origin = NSPoint( thisOriginX, thisOriginY )
	returnRect.size.width  = thisTopRightX - thisOriginX
	returnRect.size.height = thisTopRightY - thisOriginY
	return returnRect

def boundsForLayer (thisLayer):
	returnRect = NSRect()
	returnRectComps = NSRect()
	returnRectPaths = NSRect()
	
	if thisLayer.paths:
		returnRectPaths = boundsForPaths (thisLayer.paths)
		if not thisLayer.components:
			return returnRectPaths
	if thisLayer.components:
		newBounds = NSRect ()
		newBounds.origin.x = 1000
		newBounds.origin.y = 1000
		newBounds.size.width = 0
		newBounds.size.height = 0
		
		for thisComponent in thisLayer.components:
			if thisComponent.bounds.origin.x < newBounds.origin.x:
				newBounds.origin = thisComponent.bounds.origin
			if thisComponent.bounds.origin.x + thisComponent.bounds.size.width > newBounds.size.width:
				newBounds.size.width = thisComponent.bounds.origin.x + thisComponent.bounds.size.width
			if thisComponent.bounds.origin.y + thisComponent.bounds.size.height > newBounds.size.height:
				newBounds.size.height = thisComponent.bounds.origin.y + thisComponent.bounds.size.height
		
		returnRectComps = newBounds
		if not thisLayer.paths:
			return returnRectComps
			
	if distance(returnRectComps.origin, NSPoint (0,0)) > distance(returnRectPaths.origin, NSPoint (0,0)):
		returnRect.origin = returnRectPaths.origin
	else:
		returnRect.origin = returnRectComps.origin

	if distance(addPoints(returnRectComps.origin, returnRectComps.size), NSPoint (0,0)) > distance(addPoints(returnRectPaths.origin, returnRectPaths.size), NSPoint (0,0)):		size = subtractPoints(addPoints(returnRectComps.origin, returnRectComps.size), returnRect.origin)
	else:
		size = subtractPoints(addPoints(returnRectComps.origin, returnRectComps.size), returnRect.origin)
	returnRect.size = NSSize (size.x, size.y)
	
	return returnRect
	
		
def centerOfRect( thisRect ):
	centerX = ( thisRect.origin.x * 2 + thisRect.size.width ) / 2.0
	centerY = ( thisRect.origin.y * 2 + thisRect.size.height ) / 2.0
	return NSPoint( centerX, centerY )
	
def countOfNodes ( pathsList ):
	count = 0
	for thisPath in pathsList:
		count += thisPath.countOfNodes()
	return count
	
def pathCombiningBoundTest (paths, tempPaths,  accentBounds, noOfNodes, level):
	global accentFound
	global tempPathsToReturn
	
	accentFound = False
	for glyphPath in paths:
		#print level, "NoOfPaths:",noOfPaths
		#print level, "paths:", paths
		#print level, "tempPaths:", tempPaths
		tempPaths.append(glyphPath)
		searchBounds = boundsForPaths (tempPaths)
		countOfTempNodes = countOfNodes (tempPaths)
		#print searchBounds
		#print accentBounds
		if round(accentBounds.size.width) + comparePrecision >= round(searchBounds.size.width) and round(accentBounds.size.width) - comparePrecision <= round(searchBounds.size.width) and round(accentBounds.size.height) + comparePrecision >= round(searchBounds.size.height) and round(accentBounds.size.height) - comparePrecision <= round(searchBounds.size.height)and countOfTempNodes == noOfNodes:
			#print level, tempPaths,"accentFound"
			accentFound = True
			return tempPaths
		else	:
			if len(paths) > 1:
				#print level, "going into recursion"
				tempList = list(paths)
				tempList.remove (glyphPath)
				tempPathsToReturn = pathCombiningBoundTest (tempList, tempPaths, accentBounds, noOfNodes, level+1)
			#else:
				#print level, "returning from recursion"
						
		#print level, accentFound
		if accentFound == True:
			return tempPathsToReturn
		
		#print level, "deleting",glyphPath	
		tempPaths.remove(glyphPath)
	return

def process( thisLayer ):
	global errorOccured
	
	pathCount = len( thisLayer.paths )
	componentCount = len( thisLayer.components )
	
	thisGlyph = thisLayer.parent
	if changeColors:
		thisGlyph.color = 999999

	try:
		if pathCount > 0 and componentCount == 0 and thisGlyph.name not in unrebuildableGlyphs:
			
			thisGlyphInfo = GSGlyphsInfo.sharedManager().glyphInfoForGlyph_( thisGlyph )
			print "--==Rebuilding", thisLayer ,"==--"
			if thisGlyphInfo == None:
				print "!!! There is no information about that glyph. Check the name."
				raise errorOccuredException
				
			if thisGlyphInfo.components == None or len(thisGlyphInfo.components) < 2:
				print "Glyph has no components"
				return
				
			################
			#BASE GLYPH 
			################
			
			baseComponent = None
			baseComponentFound = False
			baseComponentIndex = 0
			
			for thisComponent in thisGlyphInfo.components:
				
				nameOfBaseGlyph = thisComponent.name
				if "." in thisGlyph.name:
					suffix = thisGlyph.name.split(".")[1]
					if suffix not in nameOfBaseGlyph and Font.glyphs[ nameOfBaseGlyph+"."+suffix ]:
						nameOfBaseGlyph += "."+suffix
					
				baseGlyph = Font.glyphs[ nameOfBaseGlyph ]
				if nameOfBaseGlyph == "idotless" and baseGlyph == None:
					print "!!! Component",nameOfBaseGlyph,"not found. Trying dotlessi"
					nameOfBaseGlyph = "dotlessi"
					baseGlyph = Font.glyphs[ nameOfBaseGlyph ]
							
				if nameOfBaseGlyph == "jdotless" and baseGlyph == None:
					print "!!! Component",nameOfBaseGlyph,"not found. Trying dotlessij"
					nameOfBaseGlyph = "dotlessj"
					baseGlyph = Font.glyphs[ nameOfBaseGlyph ]
					
					
				if "." in  nameOfBaseGlyph: 
					glyphName, suffix = nameOfBaseGlyph.split(".")
					if suffix == "numr" and not Font.glyphs[ nameOfBaseGlyph ] and Font.glyphs[ glyphName+".numerator" ]:
						nameOfBaseGlyph = glyphName+".numerator"
						baseGlyph = Font.glyphs[ nameOfBaseGlyph ] 
						
					if suffix == "dnom" and not Font.glyphs[ nameOfBaseGlyph ] and Font.glyphs[ glyphName+".denominator" ]:
						nameOfBaseGlyph = glyphName+".denominator"
						baseGlyph = Font.glyphs[ nameOfBaseGlyph ]
						
				if baseGlyph == None:
					print "!!! Component",nameOfBaseGlyph,"not found. Trying other components"
				else:	
					print "baseGlyph =",nameOfBaseGlyph
					baseComponent = thisComponent
					baseComponentFound = True
					break
				baseComponentIndex += 1 
			
			if baseComponentFound == False:
				print "!!! No base glyph found for", thisGlyph.name
				raise errorOccuredException
				
			baseGlyphLayer = baseGlyph.layers[ thisLayer.associatedMasterId ].copyDecomposedLayer()
			thisGlyphLayer = thisGlyph.layers[ thisLayer.associatedMasterId ]
			
			################
			#combine every path of thisGlyph to each other to find if any combination matches baseGlyph
			#actualBaseGlyphPath are the paths found
			################
			
			tempPaths = []
			accentFound = False

			baseGlyphBounds = boundsForLayer(baseGlyphLayer)
			actualBaseGlyphPath = pathCombiningBoundTest (thisLayer.paths , tempPaths, baseGlyphBounds, countOfNodes(baseGlyphLayer.paths), 0)
			
			#print actualBaseGlyphPath
			
			if actualBaseGlyphPath and len(actualBaseGlyphPath) != 0:
				baseComponenFound = True
			else:
				print "!!! baseGlyph does not equal to ",nameOfBaseGlyph,", rebuild not complete."
				raise errorOccuredException
				
			################
			# restOfPaths = thisGlyph paths - found baseGlyphPaths
			################
			
			restOfPaths = list(thisGlyphLayer.paths)
			for thisPath in actualBaseGlyphPath:
				for thatPath in thisGlyphLayer.paths:
					#print thisPath
					#print thatPath
					
					if thisPath == thatPath:
						restOfPaths.remove(thisPath)
					#	print "removed"
					#print "------"
				
			#print len(baseGlyphLayer.paths)
			#print actualBaseGlyphPath
			#print restOfPaths 
			
			################
			#ACCENTS 
			################
			accentComponents = []
			accentComponentIndex = 0
			for 	thisComponent in thisGlyphInfo.components:
				if accentComponentIndex != baseComponentIndex:
					accentInfo = thisComponent
					nameOfAccent = accentInfo.name
					
					############
					#EXCEPTIONS
								
					#print nameOfAccent
					#delete comb from name if not present
					if "comb" in nameOfAccent and Font.glyphs[ nameOfAccent ] == None:
						nameOfAccent = nameOfAccent.split('comb')[0] + nameOfAccent.split('comb')[1]
					
					#change cedilla for commaaccent with T and t
					if nameOfBaseGlyph == "T" or nameOfBaseGlyph == "t":
						if nameOfAccent == "cedilla":
							print "commaaccentcomb"
							nameOfAccent = "commaaccentcomb"
							
					if nameOfBaseGlyph == "g":
						if nameOfAccent == "commaturnedabove" and Font.glyphs[ nameOfAccent ] == None:
							print "!!! Accent commaturnedabove not present"
							raise errorOccuredException
							
					if "." in  nameOfAccent: 
						glyphName, suffix = nameOfAccent.split(".")
						if suffix == "numr" and not Font.glyphs[ nameOfAccent ] and Font.glyphs[ glyphName+".numerator" ]:
							nameOfAccent = glyphName+".numerator"
						
						if suffix == "dnom" and not Font.glyphs[ nameOfAccent ] and Font.glyphs[ glyphName+".denominator" ]:
							nameOfAccent = glyphName+".denominator"
							
					if nameOfAccent.endswith(".case"):
						if not Font.glyphs[ nameOfAccent ]:
							tempNameOfAccent = nameOfAccent.split(".case")
							nameOfAccent = tempNameOfAccent [0]
							
					if thisLayer.parent.name.endswith(".sc") and Font.glyphs[ nameOfAccent+".sc" ]:
						nameOfAccent = nameOfAccent+".sc"					
					# if uppercase accents are present find out their suffix
					if uppercaseAccentSuffix != "":
						if baseGlyph.subCategory == "Uppercase":
							tempNameOfAccent = nameOfAccent+uppercaseAccentSuffix
							#print tempNameOfAccent
							if Font.glyphs[ tempNameOfAccent ]:
								nameOfAccent = tempNameOfAccent

					print nameOfAccent
					accent = Font.glyphs[ nameOfAccent ]
					if accent == None:
						print "!!! No",nameOfAccent,"accent found, continuing search..."
						raise errorOccuredException
						
					print "Accent =", nameOfAccent
					
					accentLayer = accent.layers[ thisLayer.associatedMasterId ].copyDecomposedLayer()
					
					if len(accentLayer.paths) == 0 and len(accentLayer.components) == 0:
						print "!!! Accent",nameOfAccent,"glyph is empty, continuing search..."
						raise errorOccuredException

					#search for accent in the rest of paths of this glyph
					tempPaths = []
					accentFound = False
					accentBounds = boundsForPaths (accentLayer.paths)
					originalAccentPaths = []
					
					originalAccentPaths = pathCombiningBoundTest (restOfPaths, tempPaths, accentBounds, countOfNodes (accentLayer.paths), 0)
					
					if originalAccentPaths == None or len(originalAccentPaths) == 0:
						print "!!! Accent", nameOfAccent,"does not equal to accent in",thisGlyph.name, ", continuing search..."
						#return of accent decomposed components and paths
						raise errorOccuredException
					else:	
						restOfPathsTemp = list(restOfPaths)
						for thisPath in originalAccentPaths:
							for thatPath in restOfPaths:
								if thisPath == thatPath:
									restOfPathsTemp.remove(thisPath)
					
						restOfPaths = restOfPathsTemp
							
						#reposition component to the path position
						centerOfAccent = centerOfRect( accentLayer.bounds )
						pathcountOfAccent = len( accentLayer.paths )

						boundsOfOriginalAccent = boundsForPaths( originalAccentPaths )
						centerOfOriginalAccent = centerOfRect( boundsOfOriginalAccent )

						offsetX = centerOfOriginalAccent.x - centerOfAccent.x
						offsetY = centerOfOriginalAccent.y - centerOfAccent.y
						offset = NSPoint( offsetX, offsetY )
						newComponent = GSComponent( nameOfAccent, offset )
						
						accentComponents.append (newComponent)
						
						#print boundsOfOriginalAccent
						#print centerOfOriginalAccent
						#print centerOfAccent
						#print offset
					
				accentComponentIndex += 1

			################
			#REBUILD 
			################
						
			thisLayer.setBackground_( thisLayer )

			thisLayer.setComponents_( None )
			thisLayer.setAnchors_( None )
			
			if baseComponenFound:
				boundsOfGlyph = boundsForPaths (actualBaseGlyphPath)
				boundsOfOriginalGlyph = boundsForPaths (baseGlyphLayer.paths)
				
				centerOfGlyph = centerOfRect( boundsOfGlyph )
				centerOfOriginalGlyph = centerOfRect( boundsOfOriginalGlyph )
				
				offsetX = round(centerOfGlyph.x - centerOfOriginalGlyph.x)
				offsetY = round(centerOfGlyph.y - centerOfOriginalGlyph.y)
				offset = NSPoint( offsetX, offsetY )
				
				baseGlyphComponent = GSComponent( nameOfBaseGlyph, offset )
				baseGlyphComponent.makeDisableAlignment()
				thisLayer.addComponent_( baseGlyphComponent )
				
			for thisComponent in accentComponents:
				thisComponent.makeDisableAlignment()
				thisLayer.addComponent_( thisComponent )
			
			print len (restOfPaths)
			if restOfPaths and len (restOfPaths) > 0:
				thisLayer.setPaths_ (restOfPaths)
			else:
				thisLayer.setPaths_( None )
				thisLayer.setHints_( None )

			print "Rebuild of", thisGlyph.name,"complete!"

			if errorOccured == True and changeColors:
				thisGlyph.color = 0

	except errorOccuredException:
		errorOccured = True
		if changeColors:
			thisGlyph.color = 0
		thisLayer.decomposeComponents()

Glyphs.clearLog()
Glyphs.font.disableUpdateInterface()

tempAcutes = []
uppercaseAccentSuffix =""

for someGlyph in Font.glyphs:
	if "acute." in someGlyph.name or "acutecomb." in someGlyph.name:
		tempAcutes.append (someGlyph.name)
		
print "acutes =", tempAcutes
								
for thisName in tempAcutes:
	tempNameOfCase = thisName.split(".")
	if tempNameOfCase[1] and tempNameOfCase[1] != "sc":
		suffix = "."+tempNameOfCase[1]
		if Font.glyphs[thisName].category == "Mark":
			uppercaseAccentSuffix = suffix
			
print "uppercaseAccentSuffix =", uppercaseAccentSuffix
			
if oneGlyph == True:
	for thisLayer in selectedLayers:
		thisGlyph = thisLayer.parent
		thisGlyph.beginUndo()
		errorOccured = False
		for glyphLayer in thisGlyph.layers:
			process( glyphLayer )
		thisGlyph.endUndo()
else:
	for thisGlyph in Font.glyphs:
		thisGlyph.beginUndo()
		errorOccured = False
		for thisLayer in thisGlyph.layers:
			process( thisLayer )
		thisGlyph.endUndo()

Glyphs.font.enableUpdateInterface()
Glyphs.showMacroWindow()