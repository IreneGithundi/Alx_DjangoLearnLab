from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# ListView - Retrieve all books
# This view handles GET requests to retrieve a list of all books in the database
class BookListView(generics.ListAPIView):
    """
    API endpoint that returns a list of all books.
    
    - HTTP Method: GET
    - URL Pattern: /books/
    - Authentication: Not required (read-only access for all users)
    - Returns: List of all books with their details
    """
    # queryset: Defines what data this view will work with
    # Book.objects.all() retrieves all book instances from the database
    queryset = Book.objects.all()
    
    # serializer_class: Specifies which serializer to use for converting
    # Book instances to JSON format
    serializer_class = BookSerializer
    
    # permission_classes: Defines who can access this view
    # AllowAny means anyone can access this endpoint without authentication
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        author = serializer.validated_data.get('author')

        if Book.objects.filter(title=title, author=author).exists():
            pass

        book = serializer.save()

        print(f"Book '{book.title}' created successfully")

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'message': 'Book Created successfully!'
                    'book': serializer.data
                }
                status=status.HTTP_201_CREATED,
                headers=headers
            )
class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint that returns details of a single book.
    
    - HTTP Method: GET
    - URL Pattern: /books/<id>/
    - Authentication: Not required (read-only access for all users)
    - Returns: Details of the book with the specified ID
    - URL Parameter: pk (primary key/ID of the book)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Note: The 'pk' (primary key) is automatically extracted from the URL
    # DRF uses it to filter the queryset and return only the matching book


# CreateView - Add a new book
# This view handles POST requests to create a new book

class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint for updating an existing book.
    
    - HTTP Methods: PUT (full update), PATCH (partial update)
    - URL Pattern: /books/<id>/update/
    - Authentication: Required (only authenticated users can update books)
    - Request Body: JSON with fields to update
    - Returns: The updated book details
    
    PUT vs PATCH:
    - PUT: Requires all fields (full replacement)
    - PATCH: Allows updating only specific fields (partial update)
    
    This view automatically:
    1. Retrieves the book with the specified ID
    2. Validates the updated data
    3. Applies changes to the database
    4. Returns the updated book data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        old_instance =self.get_object()
        old_title = old_instance.title
        
        book = serializer.save()

        if old_title != book.title:
            print(f"Book '{old_title}' updated to '{book.title}'")

        def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(
                {
                    'message': 'Book updated successfully!',
                    'book': serializer.data
                }
            )
        
        def partial_update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
class BookDeleteView(generics.DestroyAPIView):
   queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
       book_title = instance.title
        book_author = instance.author.name
        
        # Log the deletion
        print(f"Deleting book: '{book_title}' by {book_author}")
        
        # Perform the actual deletion
        instance.delete()
        
        # Store the info for the response (we'll access it via instance)
        self.deleted_book_info = {
            'title': book_title,
            'author': book_author
        }
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to provide custom response.
        """
        instance = self.get_object()
        
        # Perform the deletion
        self.perform_destroy(instance)
        
        # Return custom response instead of empty 204
        return Response(
            {
                'message': 'Book deleted successfully!',
                'deleted_book': self.deleted_book_info
            },
            status=status.HTTP_200_OK  # Using 200 instead of 204 to include response body
        )