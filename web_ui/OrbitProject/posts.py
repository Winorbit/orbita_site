import requests
import json
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from .import users
from . import endpoints
from . import template_adresses

def posts(request):
    posts_response = requests.get(endpoints.POSTS_ENDPOINT)
    posts_data = posts_response.json()
    return render(request, template_adresses.POSTS_PAGE,{'posts':posts_data})
    pass

def single_post(request, id):
    post_response = requests.get(f"{endpoints.POSTS_ENDPOINT}/{id}")
    post_data = post_response.json()
    return render(request, template_adresses.SINGLE_POST_PAGE,{'post':post_data})
    pass








