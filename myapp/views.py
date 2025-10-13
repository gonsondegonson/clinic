from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from .forms import AppLogin

def appLogin(request, site):
    # Initialize error list
    errors = []
    # Get a two-digit Company Id
    idCompany = ('00' + str(site.company.id))[1:]

    if request.method == "POST":
        form = AppLogin(request.POST)

        if 'login' in request.POST:
            # Login requested
            username = request.POST.get("username")
            password = request.POST.get("password")

            if username == '' or password == '':
                errors.append("Introduzca nombre de usuario y contraseña.")
            else:
                username = username.lower() + '@' + idCompany
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect("/private")
                else:
                    errors.append("Usuario o contraseña inválidos.")
        else:
            # Operation cancelled
            return redirect("/")
    else:
        form = AppLogin()

    return render(request, 'private/login.html', {'form': form, 'errors': errors, 'site': site,})


def appLogout(request):

    logout(request)
    return redirect("/")


