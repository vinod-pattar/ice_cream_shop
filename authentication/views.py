from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Replace 'home' with your redirect URL

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your redirect URL
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, "login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Replace 'home' with your redirect URL
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Replace with your login URL
    return render(request, "register.html")
@login_required(login_url='login')
def logout_view(request):
    # Call the logout function to log out the user
    logout(request)
    # Redirect to a specified page after logout, such as the home page
    return redirect('home')  # Replace 'home' with the name of your home view

@login_required(login_url='login')
def profile_view(request):
    return render(request, "profile.html")