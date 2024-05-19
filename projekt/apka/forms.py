# forms.py
from django import forms
from .models import Post, User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    hashtags = forms.CharField(max_length=200, required=False, help_text='Enter hashtags separated by commas')
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'hashtags']

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
