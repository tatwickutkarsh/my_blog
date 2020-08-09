from .models import Post, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Profile
class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('title','text','attach_photo')
        
'''class LoginUser(forms.ModelForm):

    class Meta:
        model=Login
        fields=('username','password',)'''
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)     

class UserForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name','last_name','username','password1','password2','email')

class RegisterForm(UserForm):
    profile_pic=forms.ImageField()
    class Meta(UserForm.Meta):
        fields= UserForm.Meta.fields+('profile_pic',)