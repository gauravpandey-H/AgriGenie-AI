from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, FarmerProfileForm

def register_view(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = FarmerProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.set_password(u_form.cleaned_data['password'])
            user.save()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form = FarmerProfileForm()
    
    return render(request, 'accounts/register.html', {'u_form': u_form, 'p_form': p_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
