from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)   # clear session
    return redirect('/')  # redirect to home


# Create your views here.
