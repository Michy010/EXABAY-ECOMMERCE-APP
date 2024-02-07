from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def sign_up(request):
    form = UserRegisterForm ()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account {username} has been created! You can now log in.')
                return redirect('accounts:SignIn')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_page (request):
    if request.method == 'POST':
        username = request.POST.get ('username')
        password = request.POST.get ('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login (request, user)
            return redirect ('GetCode:profile')
        else:
            messages.error(request, 'password or username is incorrect!')

    return render (request, 'accounts/sign in.html')

@login_required
def my_center (request):
    unique_id = None  # Default to None if the user is not authenticated
    if request.user.is_authenticated:
        unique_id = request.user.unique_id

    username = request.user.username if request.user.is_authenticated else None
    return render (request, 'GetCode/my_center.html', {'unique_id':unique_id, 'username':username})