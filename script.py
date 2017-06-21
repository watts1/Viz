import pandas as pd
import numpy as np
import sys


class CreditList:
	def __init__(self):
		self.cList = []

	def addImport(self, name, imp):
		for idx, credit in enumerate(self.cList):
			if credit.name == name:
				self.cList[idx].imports.append(imp)
		
	def toJson(self, fileName):
		f1 = open(fileName, 'w+')
		f1.write('[\n')
		for row in self.cList:
			#Make include string
			#if len(row.imports)
			include_string = ','.join('"{0}"'.format(w) for w in row.imports)
			#print include_string
			f1.write('{\"name\":\"'+row.name+'\",\"size\":0,\"imports\":['+include_string+']},\n')
		f1.write(']\n')
		#REMOVE THE LAST COMMA!!!!
		
class CreditEntry:
	def __init__(self, name, type):
		self.name = name
		self.type = type
		self.imports = []
		
	def display(self):
		print self.name# + ','.join(self.imports)
		print len(self.imports)
		#Append each thing to the string to form a JSON line
		
#[
#{"name":"flare.analytics.cluster.AgglomerativeCluster","size":3938,"imports":["flare.animate.Transitioner","flare.vis.data.DataList","flare.util.math.IMatrix","flare.analytics.cluster.MergeEdge","flare.analytics.cluster.HierarchicalCluster","flare.vis.data.Data"]},
#{}
#]

def main():
	if len(sys.argv) < 1:
		print "Usage: python script.py credits.csv"
		sys.exit(1)
		
	credits = pd.read_csv(sys.argv[1])

	Cred = CreditList()
	
	for idx, col in enumerate(credits.columns):
		#Skip the name columns
		if idx < 3:
			continue
		#
		if idx < 28:
			Cred.cList.append(CreditEntry(col, "task"))
			continue
		if idx < 39:
			Cred.cList.append(CreditEntry(col, "country"))
			continue
		Cred.cList.append(CreditEntry(col, "track"))

	for index in credits.iterrows():
		Cred.cList.append(CreditEntry(index[1]['FULL NAME'], "person"))
		
		#If the person worked on a track, add the track to imports
		for i,track in enumerate(index[1][38:49]):
			if track == 1:
				Cred.addImport(index[1]["FULL NAME"], credits.columns[38+i])
				#print index[1]["FULL NAME"]
				#print credits.columns[38+i]
		#For each task and Country, add them imports of that person
		for i,track in enumerate(index[1][2:38]):
			if track == 1:
				Cred.addImport(credits.columns[2+i],index[1]["FULL NAME"])
				#print index[1]["FULL NAME"]
				#print credits.columns[27+i]
		#for tc in index[1][3:39]:
	
	#for n in Cred.cList:
		#n.display()
	
	#Print to file
	Cred.toJson("flare.json")
	
if __name__== "__main__":main()