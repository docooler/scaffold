#!/usr/bin/python

import os
import os.path
import sys
import re

rootdir = "/repo/elaiyan/radio-stubb"

class FilterHead(object):
	"""docstring for FilterHead"""
	def __init__(self, rootdir):
		super(FilterHead, self).__init__()
		self.rootdir = rootdir
		self.headFullPathFiles = []
		self.headFiles = []
		self.repeatHead = []
		self.headMap  = {}
		self.ccFiles   = []
		self.usedHead  = []
		self.ccUsedHead = []
		self.hUsedHead = []

	def getAllFiles(self, path):
		for parent, dirnames, filenames in os.walk(path):
			for dirname in dirnames:
				self.getAllFiles(parent+dirname)
			for filename in filenames:
				fullPath = os.path.join(parent, filename)
				#if this file is a soft link skip 
				if os.path.islink(fullPath):
					continue
				#this is head file
				if filename.endswith(".h"):					
					self.headFullPathFiles.append(fullPath)
					if filename in self.headFiles:
						print "error same name"
						print fullPath
						print self.headMap[filename]
						self.repeatHead.append(filename)
						continue
					self.headFiles.append(filename)
					self.headMap[filename] = fullPath
				#this is cc file
				if filename.endswith(".cc"):
					self.ccFiles.append(fullPath)

				#the sig file same as cc file
				if filename.endswith(".sig"):
					self.ccFiles.append(fullPath)
				
	def filter(self):
		print "hello filer"
		print "filter done"
	def fileterUsedHead(self):
		self.filterHeadUsedInCCFile()
		self.filterHeadUsedInHeadFile()
		self.mergeUsedHead()

	def mergeUsedHead(self):
		for h in self.ccUsedHead:
			self.usedHead.append(h)
		for h in self.hUsedHead:
			self.usedHead.append(h)

	def addCCUsedHead(self, heads):
		for head in heads:
			if head not in self.ccUsedHead:
				self.ccUsedHead.append(head)

	def addHUsedHead(self, heads):
		firstAdd = []
		for head in heads:
			if head not in self.ccUsedHead and head not in self.hUsedHead:
				self.hUsedHead.append(head)
				firstAdd.append(head)
		return firstAdd

	def filterHeadUsedInCCFile(self):
		for cc in self.ccFiles:
			heads = self.filterHeadUsedInFile(cc)
			self.addCCUsedHead(heads)


	def filterHeadUsedInFile(self, filename):
		usedHead = []
		with open(filename, 'r') as f:
			for line in f.readlines():
				secondSplit = 0
				line.strip()
				if line.find("include")>0:
					# print "debug:" + line
					tmp = line.split("\"")
					
					if len(tmp)<2:
						tmp = line.split("<")
						secondSplit = 1
						
					#this isn't a include head file
					if len(tmp) < 2:
						continue

					headFile = tmp[1]

					if secondSplit == 1:
						tmp1 = tmp[1]
						headFile = tmp1.split(">")[0]

					if headFile in self.headFiles:
						if headFile not in usedHead:
							usedHead.append(headFile)
			return usedHead
	def filterHeadUsedInHeadFile(self):
		fileStack = self.ccUsedHead[:]

		while len(fileStack)>0:
			hFile = fileStack.pop()
			heads = self.filterHeadUsedInFile(self.headMap[hFile])
			firstAdd = self.addHUsedHead(heads)
			for h in firstAdd:
				fileStack.append(h)
				
	def printArray(self, arr):
		for tmp in arr:
			print tmp

	def isRepeatFileUsed(self):
		used = False
		for h in self.repeatHead:
			if h in self.usedHead:
				used = True
				print h
		return used

							
	def run(self):
		self.getAllFiles(self.rootdir)
		
		print "=" * 100
		print "get repeat file"
		print len(self.repeatHead)
		print "cc files"
		print len(self.ccFiles)
		print "find used head file"
		self.fileterUsedHead()
		print "=" * 100
		print "repeat file used"
		self.isRepeatFileUsed()
		print "=" * 100
		self.outPutInfo()
		
		 
	def removeUnusedHead(self):
		for h in self.headFiles:
			if h not in self.usedHead:
				os.remove(self.headMap[h])
	def outPutInfo(self):
		print "=" * 100
		print ".cc file used head"
		self.printArray(self.ccUsedHead)
		print "=" * 100
		print ".h file used head"
		self.printArray(self.hUsedHead)
		print "=" * 100
		print "All head file"
		print len(self.headFiles)
		print "used head file"
		print len(self.usedHead)
		print "=" * 100
		self.removeUnusedHead()
		print "done"


def main():
	fh = FilterHead(rootdir)
	fh.run()

if __name__ == '__main__':
	main()		

