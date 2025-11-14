from bookshelf.models import Book
book_retrieve = Book.objects.all()
print(f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}")

<!-- Title: 1984, Author: George Orwell, Publication Year: 1949 -->