from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

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
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return (f"{self.user}, {self.role}")
    
class CustomUserManager(BaseUserManager):
       
       def create_user(self, username, email, password=None, **extra_fields):
           if not email:
               raise ValueError('The Email field must be set')
           
           email = self.normalize_email(email)
           user = self.model(username=username, email=email, **extra_fields)
           user.set_password(password)  # This hashes the password
           user.save(using=self._db)
           return user
       
       def create_superuser(self, username, email, password=None, **extra_fields):
           extra_fields.setdefault('is_staff', True)
           extra_fields.setdefault('is_superuser', True)
           extra_fields.setdefault('is_active', True)
           
           if extra_fields.get('is_staff') is not True:
               raise ValueError('Superuser must have is_staff=True.')
           if extra_fields.get('is_superuser') is not True:
               raise ValueError('Superuser must have is_superuser=True.')
           
           return self.create_user(username, email, password, **extra_fields)

class CustomerUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()