from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

<!-- There is no output on successful creation -->

book_retrieve = Book.objects.all()
print(f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}")

<!-- Title: 1984, Author: George Orwell, Publication Year: 1949 -->


book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

<!-- Nineteen Eighty-Four -->

book.delete()
print(Book.objects.all().count())

<!-- (1, {'bookshelf.Book': 1})
0 -->