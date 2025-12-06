from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)

        print(f"Books by {author_name}:")
        for book in books:
            print(book.title)
        
        return books
    
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()

        print(f"\nBooks in {library_name}:")
        for book in books:
            print(book.title)

        return books

    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []
    
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian

        print(f"\nLibrarian of {library_name}: {librarian.name}")

        return librarian

    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None