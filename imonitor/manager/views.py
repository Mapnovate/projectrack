from django.shortcuts import render
from manager.models import *
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.

def department_detail(request):	
	department = get_object_or_404(Departments)
	project = get_object_or_404(Projects)
	return render_to_response('departments.html', {'department': department, 'project':project})
