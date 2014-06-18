font = CurrentFont()


for groupName in font.groups.keys():
	# maybe test this before
	# in this example the group name is "@GRP_L_O"
	if groupName.startwith('@GRP'):
		mark, leftRight, keyGlyph = groupName.split("_")

		# check if the key glyph is in the font
		if keyGlyph in font:

			keyGlyph = font[keyGlyph]

			# get all the glyphs from the group
			glyphs = font.groups[groupName]

			# loop over all the glyphs
			for destGlyph in glyphs:
				# check if the destination glyph is in the font
				if destGlyph in font:

					# get the destination glyph
					destGlyph = font[destGlyph]
		
					# based on the left or right copy the margins from the key glyph
					if leftRight == "L":
						destGlyph.leftMargin = keyGlyph.leftMargin

					elif leftRight == "R":
						destGlyph.rightMargin = keyGlyph.rightMargin