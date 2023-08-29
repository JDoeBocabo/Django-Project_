from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse


def homePage(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs': blogs})


def userLogout(request):
    logout(request)
    return redirect('login')


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            errorMessage = 'Wrong Username or Password'
            return render(request, 'logIn.html', {'errorMessage': errorMessage})
    return render(request, 'logIn.html')


def signUp(request):
    form = UserRegister()
    if request.method == 'POST':
        # Create a form instance using the submitted data
        form = UserRegister(request.POST)
        # Validate the form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'Register.html', {'form': form})


@login_required
def addBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Assign the logged-in user as the author
            blog.save()
            return redirect('home')
    return render(request, 'CreateBlog.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(Profile, username=username)
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfilePictureForm(instance=user)

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'profile.html', context)


@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Relogin with your new password')
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'changePassword.html', {'form': form})


@login_required
def changeProfilePicture(request, username):
    if request.method == 'POST':
        form = ProfilePictureForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfilePictureForm()

    return render(request, 'changeProfilePicture.html', {'form': form})


def editProfile(request, username):
    form = EditProfileForm(instance=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)

    return render(request, 'editProfile.html', {'form': form})


def deleteAccount(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')
    return render(request, 'deleteAccount.html')


def blogs(request, slug):
    # read/retrieve blogs from db
    context = Blog.objects.get(slug=slug)
    return render(request, 'blog.html', {'context': context})


def updateBlog(request, slug):
    post = Blog.objects.get(slug=slug)  # get the post from db using it's slug
    form = BlogForm(instance=post)
    # form validation
    if request.method == 'POST':
        # pick the blog that is slected to be updated
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blogs', slug)  # go back to read blog
    return render(request, 'updateBlog.html', {'form': form})


def deleteBlog(request, slug):
    post = Blog.objects.get(slug=slug)
    post.delete()
    return redirect('home')


def search(request):
    query = request.GET.get('query')
    blogs = Blog.objects.filter(Q(title__icontains=query) | Q(
        author__username__icontains=query))
    context = {'blogs': blogs, 'query': query}
    return render(request, 'search.html', context)
