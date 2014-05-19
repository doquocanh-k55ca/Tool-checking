from django import forms

class CheckingForm(forms.Form):
	locationsOne = forms.CharField()
	locationsTwo = forms.CharField()
	'''
	inputsOne = forms.CharField()
	inputsTwo = forms.CharField()

	outputsOne = forms.CharField()
	outputsTwo = forms.CharField()
	
	'''
	initialStateOne = forms.CharField()
	initialStateTwo = forms.CharField()
	
	transitionsOne = forms.CharField()
	transitionsTwo = forms.CharField()

	lsFunctionsOne = forms.CharField()
	lsFunctionsTwo = forms.CharField()

	ltFunctionsOne = forms.CharField()
	ltFunctionsTwo = forms.CharField()
