from django.contrib import admin
from .models import Category, Topic, Post, ChatMessage

# Register the models
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(ChatMessage)  # Dit toevoegen
