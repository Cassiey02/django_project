from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comment, User


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'location',
            'category',
            'pub_date',
            'image',
            'is_published',
        ]
        widget = {'author': forms.HiddenInput}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'post': widgets.HiddenInput}
