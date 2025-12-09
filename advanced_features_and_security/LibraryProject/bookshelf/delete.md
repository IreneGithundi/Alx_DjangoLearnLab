from bookshelf.models import Book
book.delete()
print(Book.objects.all().count())

<!-- (1, {'bookshelf.Book': 1})
0 -->