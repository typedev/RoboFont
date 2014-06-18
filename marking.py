fea = """
mark uni0300.cap 0 678;
mark uni0301 0 508;
mark uni0301.cap 0 678;
mark uni0302 0 508;
mark uni0302.cap 0 678;
mark uni0303 0 508;
mark uni0303.cap 0 678;
mark uni0304 0 508;
mark uni0304.cap 0 678;
mark uni0306 0 508;
mark uni0306.cap 0 678;
mark uni0307 0 508;
mark uni0307.cap 0 678;
mark uni0308 0 508;
mark uni0308.cap 0 678;
mark uni0309 0 508;
mark uni0309.cap 0 678;
mark uni030A 0 508;
mark uni030A.cap 0 678;
mark uni030B 0 508;
mark uni030B.cap 0 678;
mark uni030C 0 508;
mark uni030C.cap 0 678;
mark uni030F 0 508;
mark uni030F.cap 0 678;
mark uni0312 0 508;
mark uni0313 0 508;
mark uni03080304 0 508;
mark uni03080304.cap 0 678;
mark uni03080301 0 508;
mark uni03080301.cap 0 678;
mark uni0308030C 0 508;
mark uni0308030C.cap 0 678;
mark uni03080300 0 508;
mark uni03080300.cap 0 678;
mark uni03020301 0 508;
mark uni03020301.cap 0 678;
mark uni03020300 0 508;
mark uni03020300.cap 0 678;
mark uni03020309 0 508;
mark uni03020309.cap 0 678;
mark uni03020303 0 508;
mark uni03020303.cap 0 678;
mark uni03060301 0 508;
mark uni03060301.cap 0 678;
mark uni03060300 0 508;
mark uni03060300.cap 0 678;
mark uni03060309 0 508;
mark uni03060309.cap 0 678;
mark uni03060303 0 508;
mark uni03060303.cap 0 678;
mark uni0326.a 0 508;
mark uni03020306 0 508;
mark uni03020306.cap 0 678;
"""
fealist = fea.split('\n')

for f in fealist:
	if f != '\n' and f !='':
		# print f
		f = f.replace('mark', 'markClass')
		f = f.replace(';','')
		a = f.split(' ')
		#print a
		linefea = '%s [%s] <anchor %s %s> @_mark0;' % (a[0], a[1], a[2], a[3])
		print linefea