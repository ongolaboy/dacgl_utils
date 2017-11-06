# -*-coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

def home(request):
    return  render(request,'dacgl/index.html')
