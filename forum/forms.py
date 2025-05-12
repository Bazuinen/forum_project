# forum/forms.py
from django import forms
from .models import Topic
from .models import Post

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']