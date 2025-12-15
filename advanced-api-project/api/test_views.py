from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from ..models import Author, Book

User = get_user_model()

# Helper function to create dummy Book data
def create_book(title, author, publication_year):
    return Book.objects.create(
        title=title, 
        author=author, 
        publication_year=publication_year
    )

class BookAPITestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        cls.author1 = Author.objects.create(name='Jane Austen')
        cls.author2 = Author.objects.create(name='George Orwell')

        cls.book1 = create_book("Pride and Prejudice", cls.author1, date(1813, 1, 28))
        cls.book2 = create_book("1984", cls.author2, date(1949, 6, 8))
        cls.book3 = create_book("Emma", cls.author1, date(1815, 12, 1))

        # Test users
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.admin = User.objects.create_superuser(username='admin', password='adminpassword')

        # URLs
        cls.list_url = reverse('api:book-list')
        cls.create_url = reverse('api:book-create')
        cls.detail_url = reverse('api:book-detail', kwargs={'pk': cls.book1.pk})
        cls.update_url = reverse('api:book-update', kwargs={'pk': cls.book1.pk})
        cls.delete_url = reverse('api:book-delete', kwargs={'pk': cls.book1.pk})

    # --- 1. BookListView (GET /books/) Tests ---
    
    def test_list_all_books(self):
        """Test that the book list view returns all books and status 200 OK."""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that all books are returned in the custom 'results' key
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)

    def test_list_with_title_filter(self):
        """Test filtering books by title using `filterset_fields`."""
        # Query parameter based on filterset_fields
        response = self.client.get(self.list_url, {'title': '1984'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
        self.assertEqual(response.data['filters_applied']['publication_year'], None)
        
    def test_list_with_search_filter(self):
        """Test searching books by author name using `search_fields`."""
        response = self.client.get(self.list_url, {'search': 'George'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
        self.assertEqual(response.data['filters_applied']['search'], 'George')
        
    def test_list_with_ordering(self):
        """Test ordering books by publication year."""
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Pride and Prejudice') # Oldest
        self.assertEqual(response.data['results'][2]['title'], '1984') # Newest (assuming the publication_year is a DateField and ordering is ascending by default)
        
    def test_list_with_custom_year_range_filter(self):
        """Test custom filtering using `year_from` and `year_to` in `get_queryset`."""
        # Filter for books published between 1900-01-01 and 2000-01-01
        response = self.client.get(self.list_url, {'year_from': '1900-01-01', 'year_to': '2000-01-01'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1) # Should only return '1984'

    # --- 2. BookCreateView (POST /books/create/) Tests ---
    
    def test_create_book_authenticated(self):
        """Test a logged-in user can successfully create a book."""
        self.client.force_authenticate(user=self.user)
        
        new_book_data = {
            'title': 'New Test Book',
            'author': self.author2.pk, # Use the primary key of an existing author
            'publication_year': '2023-01-01'
        }
        response = self.client.post(self.create_url, new_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        
    def test_create_book_unauthenticated_fails(self):
        """Test unauthenticated user cannot create a book (IsAuthenticated required)."""
        new_book_data = {
            'title': 'Unauthorized Book',
            'author': self.author1.pk,
            'publication_year': '2024-01-01'
        }
        response = self.client.post(self.create_url, new_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3) # Count should remain the same
        
    def test_create_book_future_year_fails(self):
        """Test validation for publication year in the future."""
        self.client.force_authenticate(user=self.user)
        tomorrow = date.today() + timedelta(days=1)
        
        bad_data = {
            'title': 'Future Book',
            'author': self.author1.pk,
            'publication_year': tomorrow.strftime('%Y-%m-%d')
        }
        response = self.client.post(self.create_url, bad_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication year cannot be in the future', str(response.data['publication_year']))
        
    # --- 3. BookDetailView (GET /books/<pk>/) Tests ---
    
    def test_retrieve_book_success(self):
        """Test retrieving a single book detail."""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Pride and Prejudice')
        
    def test_retrieve_nonexistent_book_fails(self):
        """Test retrieving a book with an invalid ID."""
        non_existent_url = reverse('api:book-detail', kwargs={'pk': 9999})
        response = self.client.get(non_existent_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- 4. BookUpdateView (PUT/PATCH /books/<pk>/update/) Tests ---
    
    def test_update_book_authenticated(self):
        """Test a logged-in user can update a book (PATCH)."""
        self.client.force_authenticate(user=self.user)
        update_data = {
            'title': 'Pride and Prejudice - Updated',
        }
        response = self.client.patch(self.update_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Pride and Prejudice - Updated')
        
        # Verify database change
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Pride and Prejudice - Updated')
        
    def test_update_book_unauthenticated_fails(self):
        """Test unauthenticated user cannot update a book (IsAuthenticated required)."""
        update_data = {
            'title': 'Should Not Update',
        }
        response = self.client.patch(self.update_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify database unchanged
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Pride and Prejudice')

    # --- 5. BookDeleteView (DELETE /books/<pk>/delete/) Tests ---
    
    def test_delete_book_authenticated(self):
        """Test a logged-in user can delete a book."""
        # Create a book to delete so we don't mess up the main test data
        book_to_delete = create_book("To Be Deleted", self.author1, date(2000, 1, 1))
        delete_url = reverse('api:book-delete', kwargs={'pk': book_to_delete.pk})
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book deleted successfully!')
        
        # Verify database change
        self.assertEqual(Book.objects.filter(pk=book_to_delete.pk).exists(), False)
        
    def test_delete_book_unauthenticated_fails(self):
        """Test unauthenticated user cannot delete a book (IsAuthenticated required)."""
        book_count_before = Book.objects.count()
        
        response = self.client.delete(self.delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), book_count_before) # Count should remain the same