from django.template import Context, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.db.models import Q
from CheckingTool.forms import *
from django.http import Http404, HttpResponseRedirect, HttpResponse
from CheckingTool.automata import *
from CheckingTool.timed_design import *
import re
from CheckingTool.preprocess import *
import json
#from pure_pagination.paginator import Paginator

import re
import z3
def Pluggability(request):
	#
	value = "None"
	if request.session.has_key('data'):
		value = request.session.get('data')
		del request.session['data']

	var = RequestContext(request,{
			"value": value
		})

	return render_to_response("pluggability.html", var)
def Refinement(request):
	return render_to_response("refiement.html", context_instance=RequestContext(request))

def Checking(request):
	if request.method == 'POST':
		form = CheckingForm(request.POST)
		#test = request.locationsOne
		if form.is_valid():
			if "pluggability" in request.POST:
				if PluggabilitySolving(Preprocess.GetData(form)) == True:
					request.session["data"] = "Yes"
				else:
					request.session["data"] = "No"
				return HttpResponseRedirect("/pluggability/")
			else:
				if RefinementSolving(form) == True:
					request.session["data"] = "Yes"
				else:
					request.session["data"] = "No" 
				return HttpResponseRedirect("/refinement/")
	else:
		form = CheckingForm() # An unbound form

	data = RequestContext(request,{
		'form': form,
	})
	return render_to_response('checking.html', data)
def PluggabilitySolving(data):
	interface = automata(locations = data["locationsOne"],
	                     inputs = set(["x"]),
	                     outputs = set(["y"]),
	                     initial_state = data["initialStateOne"],
	                     transitions = data["transitionsOne"],
	                     ls = data["lsFunctionsOne"],
	                     lt = data["ltFunctionsOne"]
	                     )

	# timed designs and guard formulas for environment
	environment = automata(locations = data["locationsTwo"],
	                     inputs = set(["x"]),
	                     outputs = set(["y"]),
	                     initial_state = data["initialStateTwo"],
	                     transitions = data["transitionsTwo"],
	                     ls = data["lsFunctionsTwo"],
	                     lt= data["ltFunctionsTwo"]
	                     )
	return 	check_plugability(interface, environment)


def RefinementSolving(form):
	return True