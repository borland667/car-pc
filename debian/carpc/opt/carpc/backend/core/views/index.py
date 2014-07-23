# coding: utf-8
from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def forbidden(request):
    return render(request, 'core/forbidden.html')