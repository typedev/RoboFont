# -*- coding: utf-8 -*-

from robofab.world import CurrentFont

font = CurrentFont()

featxt = font.features.text
featxt = ' '.join(featxt.split()).split(';')
for id, line in enumerate(featxt):
	line = line.strip()
	if line.startswith('@'):
		a = line.split(' ')
		groupname = a[0].replace('@','')
		a.remove('=')
		a.remove('[')
		a.remove(']')
		content = a[1:]
		# print groupname, '>', content

		print 'New group created: ' + groupname
		font.groups[groupname] = content
