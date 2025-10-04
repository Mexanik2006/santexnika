from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard/")
    else:
        # Widget attrs qo'shib, input'larga Tailwind sinflarini beramiz
        form = AuthenticationForm(
            request,
            {
                'username': {'attrs': {'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-border placeholder-muted-foreground text-foreground rounded-t-md focus:outline-none focus:ring-accent focus:border-accent focus:z-10 sm:text-sm bg-background'}},
                'password': {'attrs': {'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-border placeholder-muted-foreground text-foreground rounded-b-md focus:outline-none focus:ring-accent focus:border-accent focus:z-10 sm:text-sm bg-background'}}
            }
        )
    
    error = form.errors.get('__all__', '') if request.method == "POST" else None
    return render(request, "account/login.html", {"form": form, "error": error})


def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required
def home(request):
    form = AuthenticationForm()
    return render(request, "account/dashboard.html", {"form": form})

@login_required
def client(request):
    form = AuthenticationForm()
    return render(request, "client/clientlist.html", {"form": form})