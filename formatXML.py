#this module is used to output a formatted 'easy on the eye' xml of the gold coref data
import processGold as prep
import sys

file=sys.argv[1]
cf=prep.mainPreprocess(file)
ps=cf.toprettyxml()
print ps
