from django.shortcuts import render
from django.http import HttpResponse

# views or requests handlers

def home_view(request):
    return HttpResponse('Welcome to PayPulse Backend !!')

def sample(request):
    return HttpResponse('Django successfully started')
  