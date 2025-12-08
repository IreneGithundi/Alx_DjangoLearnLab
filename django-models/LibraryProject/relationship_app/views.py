from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerUserCreationForm
from django.contrib.auth.forms import UserCreationForm 
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = CustomerUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin, login_url='/access-denied/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

@user_passes_test(is_librarian, login_url='/access-denied/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

@user_passes_test(is_member, login_url='/access-denied/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })