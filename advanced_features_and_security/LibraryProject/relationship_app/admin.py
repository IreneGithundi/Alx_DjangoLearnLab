from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile



class CustomUserAdmin(UserAdmin):
    
    model = CustomUser
    
    list_display = [
        'username',        # Username column
        'email',           # Email column
        'first_name',      # First name column
        'last_name',       # Last name column
        'is_staff',        # Staff status column
        'is_active',       # Active status column
        'date_of_birth',   # Our custom field - birth date column
    ]
    
   
    list_filter = [
        'is_staff',        # Filter by staff status
        'is_superuser',    # Filter by superuser status
        'is_active',       # Filter by active status
        'groups',          # Filter by groups
    ]
    
    
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    
    
    ordering = ['username']
    
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
            'description': 'Optional fields for user profile'
        }),
    )
    
   
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
            'description': 'Optional fields for user profile'
        }),
    )



admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['author']
    search_fields = ['title', 'author__name']


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['books'] 


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library']
    search_fields = ['name', 'library__name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']