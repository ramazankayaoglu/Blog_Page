from django.http import HttpResponseBadRequest
from django.shortcuts import reverse,HttpResponseRedirect
from django.contrib.auth import authenticate

def is_post(func):
    def wrap(request,*args,**kwargs):
        if request.method == 'GET':
            return HttpResponseBadRequest
        return func(request,*args,**kwargs)
    return wrap

def anonymous_required(func):
    def wrap(request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("posts:list"))
        return func(request,*args,**kwargs)
    return wrap