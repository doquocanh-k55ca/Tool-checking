from django.conf.urls import patterns, include, url

urlpatterns = patterns('CheckingTool.views',
	url(r'^check/$','Checking'),
	url(r'^refinement/$','Refinement'),
	url(r'^pluggability/$','Pluggability'),

)