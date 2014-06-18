
# listStems string: 10 20 30 40=0 50 60 70 80 90 100=1 110 120

ListManualStems = '48=0 74 94 128 165 192 218=1'

def getFactorByStem (minStem, maxStem, midStem):
	if (midStem != 0) and (midStem != 1000):
		return 1000 * (midStem - minStem) / (maxStem - minStem)
	else:
		return midStem


def getFactorListByStems (listStems):
	ld = listStems.split(' ')
	ls = []
	lf = []
	for i in ld:
		if '=' in i:
			lm = i.split('=')
			if lm[1] == '0':
				minStem = int(lm[0])
				ls.append(0)
			if lm[1] == '1':
				maxStem = int(lm[0])
				ls.append(1000)
		else:
			ls.append(int(i))
	for i in ls:
		lf.append(getFactorByStem(minStem, maxStem, i) / 1000.0)
	return lf

stemslist = ListManualStems.split(' ')
for idx, value in enumerate(stemslist):
	print 'stem\t', value
	print 'factor\t',getFactorListByStems(ListManualStems)[idx]
# print ListManualStems.split(' ')
# print getFactorListByStems(ListManualStems)