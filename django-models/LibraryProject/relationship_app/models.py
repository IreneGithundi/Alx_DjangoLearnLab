from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book entry"),
            ("can_change_book", "Can change an existing book entry"),
            ("can_delete_book", "Can delete a book entry"),
        ]
        
    def __str__(self):
        return (f"{self.title}, {self.author},")
    
class Library(models.Model):
    name=models.CharField(max_length=50)
    books=models.ManyToManyField(Book)

    def __str__(self):
        return (f"{self.name}, {self.books}")

class Librarian(models.Model):
    name=models.CharField(max_length=50)
    library=models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.name}, {self.library}")
    
class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    )
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return (f"{self.user}, {self.role}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()