import requests
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from poetryapp.models import Profile



def home(request):
    return render(request, 'poetryapp/home.html')  


def search_poem(request):
    query = request.GET.get('q', '')  
    poems = []

    if query:
        # Try author search
        url = f"https://poetrydb.org/author/{query}"
        response = requests.get(url)
        data = response.json()

        # Only use data if it's a list (valid poems)
        if isinstance(data, list):
            poems = data
        else:
            # Try title search
            url = f"https://poetrydb.org/title/{query}"
            response = requests.get(url)
            data = response.json()
            if isinstance(data, list):
                poems = data

    # Pagination logic
    paginator = Paginator(poems, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'poetryapp/search_results.html', {
        'poems': page_obj,
        'query': query
    })

def poem_detail(request, title):
    # Assuming the API returns a list with the poem details
    url = f"https://poetrydb.org/title/{title}"
    response = requests.get(url)
    poem = response.json()

    if not poem:
        return render(request, 'poetryapp/poem_not_found.html', {'title': title})

    return render(request, 'poetryapp/poem_detail.html', {'poem': poem[0]})

def signup_views(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'poetryapp/signup.html', {'form' : form})

def login_view(request):
    if request.method== 'POST':
        username =  request.POST['username']
        password =  request.POST['password']

        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'poetryapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'poetryapp/profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page
    else:
        form = EditProfileForm(instance=profile)
    
    return render(request, 'poetryapp/edit_profile.html', {'form': form})

def write_poem(request):
    return render(request, 'poetryapp/write_poem.html')