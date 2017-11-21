# -*-coding:utf-8 -*-

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def home(request):
    return  render(request,'dacgl/index.html')

def entree(request):
    return render(request,'dacgl/entree.html')

def sortie(request):
    logout(request)
    return HttpResponseRedirect(reverse('sortie'))
