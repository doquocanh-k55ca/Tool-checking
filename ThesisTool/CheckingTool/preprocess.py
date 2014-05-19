import re
from CheckingTool.timed_design import *
class Preprocess(object):

	rTransition = re.compile(r'(\w+,\w+)')
	rTimeDesign = re.compile(r'(\w+,\w+,(\d+,\d+))')
	"""docstring for ClassName"""
	def __init__(self):
		pass
	
	@staticmethod
	def GetLocations(input):
		return set(input.split(","))
	
	@staticmethod
	def GetTransitions(input):
		transitions = set()
		for s_trans in Preprocess.rTransition.findall(input):
			trans = s_trans.split(",")
			transitions.add((trans[0],trans[1]))
		return transitions
	
	@staticmethod
	def GetInitialState(input):
		return input
	
	
	@staticmethod
	def GetLsFunctions(input, locations):
		lsFunctions = {}
		list_ls = input.split(":")
		listLocations = locations.split(",")
		for ls in list_ls:
			listTimedDesign = ls.split(';')
			timeMatch = re.compile(r'(\d+,\d+)').findall(listTimedDesign[2])[0]
			timedDesign = timed_design(listTimedDesign[0],listTimedDesign[1],(int(timeMatch[0]),int(timeMatch[2])))
			lsFunctions[listLocations[list_ls.index(ls)]] = timedDesign
		return lsFunctions
	
	
	@staticmethod
	def GetLtFunctions(input, inputTransitions):
		list_lt = input.split(":")
		ltFunctions = {}

		transitions = []
		for s_trans in Preprocess.rTransition.findall(inputTransitions):
			trans = s_trans.split(",")
			transitions.append((trans[0],trans[1]))
		listTransitions = list(transitions)
		
		index = 0
		for lt in list_lt:
			ltFunctions[listTransitions[index]] = list_lt[index]
			index += 1
		return ltFunctions
	@staticmethod
	def GetData(formInput):
		inp = formInput.cleaned_data
		data = {}	

		data["locationsOne"] = Preprocess.GetLocations(inp['locationsOne'])
		data["locationsTwo"] = Preprocess.GetLocations(inp['locationsTwo'])

		data["initialStateOne"] = Preprocess.GetInitialState(inp['initialStateOne'])
		data["initialStateTwo"] = Preprocess.GetInitialState(inp['initialStateTwo'])
		
		data["transitionsOne"] = Preprocess.GetTransitions(inp['transitionsOne'])
		data["transitionsTwo"] = Preprocess.GetTransitions(inp['transitionsTwo'])

		data["lsFunctionsOne"] = Preprocess.GetLsFunctions(inp['lsFunctionsOne'],inp["locationsOne"])
		data["lsFunctionsTwo"] = Preprocess.GetLsFunctions(inp['lsFunctionsTwo'],inp["locationsTwo"])

		data["ltFunctionsOne"] = Preprocess.GetLtFunctions(inp['ltFunctionsOne'],inp['transitionsOne'])
		data["ltFunctionsTwo"] = Preprocess.GetLtFunctions(inp['ltFunctionsTwo'],inp["transitionsTwo"])
		#data["Ok"] = Preprocess.XXX()
		return data
		