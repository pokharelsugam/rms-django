from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

def user_management(request):
    return render(request, 'user-management.html')


def login_universal(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now successfully logged in as {username}.")
                return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_universal(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to login page after logout

@login_required
def register_universal(request):
    if not (request.user.is_admin or request.user.is_manager) :
        return HttpResponse("Unauthorized! Please login with admin or manager account to access full features", status=401)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)
