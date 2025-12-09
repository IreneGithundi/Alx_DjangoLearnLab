from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Book
from .forms import BookForm, ExampleForm  # Import your forms

# ============================================================================
# SECURITY BEST PRACTICES IN VIEWS
# ============================================================================

# View to list all books with search functionality
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books with optional search functionality.
    
    SECURITY MEASURES:
    - Uses Django ORM to prevent SQL injection
    - Validates and sanitizes search input through Django's query methods
    - User input is never directly interpolated into SQL queries
    """
    books = Book.objects.all()
    
    # SECURE: Handle search query safely using Django ORM
    search_query = request.GET.get('search', '')
    
    if search_query:
        # SAFE: Using Django ORM's filter with Q objects
        # This is parameterized and prevents SQL injection
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
        
        # UNSAFE EXAMPLE - NEVER DO THIS:
        # from django.db import connection
        # cursor = connection.cursor()
        # cursor.execute(f"SELECT * FROM books WHERE title LIKE '%{search_query}%'")
        # This is vulnerable to SQL injection!
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    
    SECURITY MEASURES:
    - Uses Django forms for input validation and sanitization
    - Form automatically escapes user input
    - CSRF protection enforced via middleware and template token
    """
    if request.method == 'POST':
        # SAFE: Django forms automatically validate and sanitize input
        form = BookForm(request.POST)
        
        if form.is_valid():
            # form.cleaned_data contains validated and sanitized data
            book = form.save()
            
            # SAFE: Using Django's redirect function
            return redirect('book_list')
        
        # If form is invalid, it will display errors in the template
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    
    SECURITY MEASURES:
    - Uses get_object_or_404 to safely retrieve objects
    - Prevents SQL injection through ORM
    - Validates primary key parameter
    - Uses Django forms for input validation
    """
    # SAFE: get_object_or_404 uses parameterized queries
    # pk is automatically validated as an integer by Django's URL routing
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        
        if form.is_valid():
            # SAFE: form.cleaned_data contains sanitized data
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Edit'
    })


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book.
    
    SECURITY MEASURES:
    - Only accepts POST requests for delete operations (safer than GET)
    - Uses ORM's delete method (parameterized)
    - Validates user has permission before deletion
    """
    # SAFE: ORM query with parameterized pk
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # SAFE: ORM delete method
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {
        'book': book
    })


# Example: Advanced search with multiple parameters
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def advanced_book_search(request):
    """
    Advanced search with multiple parameters.
    
    SECURITY MEASURES:
    - All user inputs are validated through Django forms or ORM methods
    - Never uses raw SQL with string formatting
    - Properly escapes all output in templates
    """
    books = Book.objects.all()
    
    # SAFE: Get and validate query parameters
    title = request.GET.get('title', '').strip()
    author = request.GET.get('author', '').strip()
    year = request.GET.get('year', '').strip()
    
    # Build query safely using Django ORM
    if title:
        books = books.filter(title__icontains=title)
    
    if author:
        books = books.filter(author__icontains=author)
    
    if year:
        # SAFE: Validate year is numeric before filtering
        try:
            year_int = int(year)
            books = books.filter(publication_year=year_int)
        except ValueError:
            # Invalid year input - ignore or show error
            pass
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books
    })


# ============================================================================
# EXAMPLES OF SECURE vs INSECURE CODE
# ============================================================================

# ❌ INSECURE EXAMPLE - DO NOT USE
def insecure_search_example(request):
    """
    THIS IS AN EXAMPLE OF WHAT NOT TO DO!
    This code is vulnerable to SQL injection.
    """
    search = request.GET.get('search', '')
    
    # DANGEROUS: Never concatenate user input directly into SQL!
    from django.db import connection
    cursor = connection.cursor()
    
    # SQL INJECTION VULNERABILITY!
    cursor.execute(f"SELECT * FROM bookshelf_book WHERE title = '{search}'")
    # An attacker could input: ' OR '1'='1' --
    # Resulting in: SELECT * FROM bookshelf_book WHERE title = '' OR '1'='1' --'
    
    return render(request, 'bookshelf/book_list.html', {})


# ✅ SECURE EXAMPLE - USE THIS
def secure_search_example(request):
    """
    This is the correct way to handle user input.
    Uses Django ORM which automatically parameterizes queries.
    """
    search = request.GET.get('search', '')
    
    # SAFE: Django ORM uses parameterized queries
    books = Book.objects.filter(title__icontains=search)
    
    # Even if you must use raw SQL, use parameterization:
    # from django.db import connection
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM bookshelf_book WHERE title = %s", [search])
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books
    })