from django.shortcuts import redirect



def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in allowedGroups:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decorator


def allowedCastomar(Castomar=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in Castomar:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('passs')
        return wrapper_func
    return decorator



def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in allowedGroups:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decorator


def aminnUsers(adminGroups=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in adminGroups:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decorator