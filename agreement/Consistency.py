#!/usr/bin/env python
# coding=utf-8

'''
@author Quanqi Yue, {@literal <quanqi.yue@leyantech.com>}
@date 2018-12-18
'''

import codecs
import re
import sys


def readFile(infile):
	with codecs.open(infile, 'r', 'utf-8') as sour:
		for line in sour:
			line = line.rstrip('\r\n')
			fields = line.split('\t')
			yield fields


def getDict(infile, column):
	d = {}
	fields = readFile(infile)
	for s in fields:
		key = s[0].strip()
		if ',' not in column and isinstance(int(column), int):
			value = s[int(column) - 1].strip()
		elif ',' in column:
			columns = column.split(',')
			value = []
			for n in columns:
				value.append(s[int(n) - 1].strip())
			value = '\t'.join(value)
		
		if key == 'query':
			continue
		else:
			d[key] = value
	return d


def consistency(dict1, dict2):
	total = min(len(dict1), len(dict2))
	consistent = 0
	i = 0
	for k, v in dict1.items():
		if k in dict2 and dict2[k] == v and i < total:
			consistent += 1
		i += 1
	consistentRate = consistent/total
	print(total, consistent)
	
	return consistentRate


def main(infile1, infile2, column):
	d1 = getDict(infile1, column)
	d2 = getDict(infile2, column)
	consistentRate = consistency(d1, d2)
	return consistentRate
	#print(infile1, infile2, consistentRate)


if __name__ == '__main__':
	#infileList = 'meizhuang_A1-2.txt,meizhuang_B1-2.txt,meizhuang_C1-2.txt'.split(',')
	infileList = 'songzi.female.txt,X.female.txt,beichen.female.txt'.split(',')
	outhead = [''] + infileList
	print('\t'.join(outhead))
	for i in range(0, len(infileList)):
		a = [infileList[i]]
		for j in range(0, len(infileList)):
			consistentRate = main(infileList[i], infileList[j], sys.argv[1])
			a.append(str(consistentRate))
		print('\t'.join(a))