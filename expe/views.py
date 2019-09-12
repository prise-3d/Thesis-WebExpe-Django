from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def expe(request):

    link1 = 'http://diran.univ-littoral.fr/api/images/bathroom/bathroom_00200.png'
    return render(request, 'expe/expe.html', {'expe_name': 'test_expe', 'link1': link1})