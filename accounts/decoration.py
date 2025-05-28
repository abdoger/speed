

from django.shortcuts import render,redirect
def allowedusers(allowGroups=[]):
    def decoratar(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in allowGroups:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('t404')
        return wrapper_func
    return decoratar


def allowedusershr(allowGroupshr =[]):
    def decoratar(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in allowGroupshr:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decoratar