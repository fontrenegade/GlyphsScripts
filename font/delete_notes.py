#MenuTitle: Delete notes
# -*- coding: utf-8 -*-
__doc__="""Delete notes"""

for thisGlyph in Glyphs.font.glyphs:
	for thisLayer in thisGlyph.layers:
		thisLayer.annotations = []
