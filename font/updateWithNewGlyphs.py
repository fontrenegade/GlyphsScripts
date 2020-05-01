#MenuTitle: Update With New Glyphs
# -*- coding: utf-8 -*-
__doc__="""Update With New Glyphs"""

import vanilla
			
class UpdateGlyphs(object):
	"""Update glyphs"""
	def __init__(self):
		self.listOfMasters = []
		self.updateListOfMasters() 

		self.w = vanilla.FloatingWindow((400, 70), "Update glyphs")
		
		self.w.text_anchor = vanilla.TextBox((15, 12+2, 130, 14), "From master:", sizeStyle='small')
		self.w.from_font = vanilla.PopUpButton((150, 12, 150, 17), self.listOfMasterNames(), sizeStyle='small', callback=self.buttonCheck)
		
		self.w.text_value = vanilla.TextBox((15, 12+2+25, 130, 14), "To master:", sizeStyle='small')
		self.w.to_font = vanilla.PopUpButton((150, 12+25, 150, 17), self.listOfMasterNames()[::-1], sizeStyle='small', callback=self.buttonCheck)

		self.w.copybutton = vanilla.Button((-80, 12+25, -15, 17), "Copy", sizeStyle='small', callback=self.updateGlyphs)
		self.w.setDefaultButton( self.w.copybutton )

		self.w.open()
		self.buttonCheck(None)
		
	def nameForID( self, Font, ID ):
		try:
			if ID[0] == "@": # is a group
				return ID
			else: # is a glyph
				return Font.glyphForId_( ID ).name
		except Exception as e:
			raise e
		
	def updateListOfMasters( self ):
		masterList = []
		
		for thisFont in Glyphs.fonts:
			for thisMaster in thisFont.masters:
				masterList.append( thisMaster )
		
		self.listOfMasters = masterList
		#print masterList
	
	def listOfMasterNames( self ):
		myMasterNameList = [ "%s - %s" % ( m.font().filepath.split("/")[-1], m.weightValue ) for m in self.listOfMasters ]
		return myMasterNameList
	
	def buttonCheck(self, sender):
		fromFont = self.w.from_font.getItems()[ self.w.from_font.get() ]
		toFont   = self.w.to_font.getItems()[ self.w.to_font.get() ]

		if fromFont == toFont:
			self.w.copybutton.enable( onOff=False )
		else:
			self.w.copybutton.enable( onOff=True )
	
	def updateGlyphs(self, sender):
		fromFontIndex = self.w.from_font.get()
		toFontIndex = (self.w.to_font.get() * -1) - 1
		
		sourceMaster   = self.listOfMasters[ fromFontIndex ]
		targetMaster   = self.listOfMasters[ toFontIndex ]
		sourceMasterID = sourceMaster.id
		targetMasterID = targetMaster.id
		sourceFont     = sourceMaster.font()
		targetFont     = targetMaster.font()
		fromFont = self.w.from_font.getItems()[ self.w.from_font.get() ]
		toFont   = self.w.to_font.getItems()[ self.w.to_font.get() ]

		print "sourceFont:", sourceFont.filepath
		print "targetFont:", targetFont.filepath

		FromGlyphs =  [g.parent.name for g in sourceFont.selectedLayers]
		print FromGlyphs
		for i in range (0, len(FromGlyphs)):
			try:
				glyphFrom = sourceFont.glyphs[FromGlyphs[i]]
				if glyphFrom:
					
					if not targetFont.glyphs[FromGlyphs[i]]:
						targetFont.glyphs.append(GSGlyph(FromGlyphs[i]))

					glyphTo = targetFont.glyphs[FromGlyphs[i]]
					glyphTo.layers[targetMasterID] = glyphFrom.layers[sourceMasterID].copy()
					layerTo = glyphTo.layers[targetMasterID]
					
					glyphTo.leftKerningGroup = glyphFrom.leftKerningGroup
					glyphTo.rightKerningGroup = glyphFrom.rightKerningGroup
												
					glyphFrom.color = 4
					glyphTo.color = 4
					print glyphFrom.name, "copied"
				else:
					print FromGlyphs[i], "does not exist in", sourceFont.filepath
					glyphFrom.color = 0
			except:
				print "Unexpected error:", sys.exc_info()[0]

		print "Done."
		#self.w.close()
		
Glyphs.clearLog()
Glyphs.font.disableUpdateInterface()			

UpdateGlyphs()

Glyphs.font.enableUpdateInterface()
Glyphs.showMacroWindow()
