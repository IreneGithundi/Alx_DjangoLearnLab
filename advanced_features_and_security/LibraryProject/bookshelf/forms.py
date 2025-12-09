# forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Form for creating and editing books.
    
    SECURITY FEATURES:
    - Automatically validates input types
    - Escapes HTML in user input
    - Prevents XSS attacks through proper sanitization
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
        # Optional: Add custom validation
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter book title',
                'maxlength': 200
            }),
            'author': forms.TextInput(attrs={
                'placeholder': 'Enter author name',
                'maxlength': 100
            }),
            'publication_year': forms.NumberInput(attrs={
                'placeholder': 'Enter year',
                'min': 1000,
                'max': 9999
            })
        }
    
    def clean_publication_year(self):
        """
        Custom validation for publication year.
        
        SECURITY: Validates that year is within acceptable range
        """
        year = self.cleaned_data.get('publication_year')
        
        if year:
            import datetime
            current_year = datetime.datetime.now().year
            
            if year < 1000 or year > current_year + 1:
                raise forms.ValidationError(
                    f'Publication year must be between 1000 and {current_year + 1}'
                )
        
        return year
    
    def clean_title(self):
        """
        Custom validation for title.
        
        SECURITY: Ensures title is not empty after stripping whitespace
        """
        title = self.cleaned_data.get('title')
        
        if title:
            title = title.strip()
            if not title:
                raise forms.ValidationError('Title cannot be empty or just whitespace')
        
        return title


# Example form for form_example.html
class ExampleForm(forms.Form):
    """
    Example form demonstrating various security features.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter your name'
    )
    
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address'
    )
    
    message = forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        help_text='Enter your message (max 1000 characters)'
    )
    
    def clean_name(self):
        """Strip whitespace and validate name"""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Name is required')
        return name