from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm  

# View to list all books - requires can_view permission
@login_required
@permission_required('bookstore.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books.
    Only users with 'can_view' permission can access this view.
    """
    books = Book.objects.all()
    return render(request, 'bookstore/book_list.html', {'books': books})

# View to create a new book - requires can_create permission
@login_required
@permission_required('bookstore.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    Only users with 'can_create' permission can access this view.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookstore/book_form.html', {'form': form, 'action': 'Create'})

# View to edit an existing book - requires can_edit permission
@login_required
@permission_required('bookstore.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    Only users with 'can_edit' permission can access this view.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookstore/book_form.html', {'form': form, 'action': 'Edit'})

# View to delete a book - requires can_delete permission
@login_required
@permission_required('bookstore.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book.
    Only users with 'can_delete' permission can access this view.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookstore/book_confirm_delete.html', {'book': book})