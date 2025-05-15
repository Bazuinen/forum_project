from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Category, Topic, Post, ChatMessage
from .forms import TopicForm, PostForm
from django.db.models import Q
from django.db.models import Count


def index(request):
    categories = Category.objects.annotate(
        num_topics=Count('topic'),
        num_posts=Count('topic__posts')
    )
    # Om laatste post per category te tonen, kun je bijvoorbeeld:
    latest_posts = {}
    for category in categories:
        # Alle posts binnen deze category's topics, gesorteerd op nieuwste
        last_post = Post.objects.filter(topic__category=category).order_by('-created_at').first()
        if last_post:
            latest_posts[category.id] = last_post

    return render(request, 'forum/index.html', {
        'categories': categories,
        'latest_posts': latest_posts,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account aangemaakt! Je kan nu inloggen.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def search(request):
    query = request.GET.get('q', '')
    topics = Topic.objects.filter(Q(title__icontains=query) | Q(posts__content__icontains=query)).distinct()
    return render(request, 'forum/search_results.html', {'topics': topics, 'query': query})

def category_topics(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = Topic.objects.filter(category=category)
    return render(request, 'forum/category_topics.html', {'category': category, 'topics': topics})

@login_required
def create_topic(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.created_by = request.user
            topic.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {'form': form, 'category': category})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = PostForm()
    return render(request, 'forum/topic_detail.html', {'topic': topic, 'posts': posts, 'form': form})

@login_required
def send_chat_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(user=request.user, message=message)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})


def get_chat_messages(request):
    chat_messages = ChatMessage.objects.all().order_by('created_at')
    messages_data = [
        {
            'user': message.user.username,
            'message': message.message,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in chat_messages
    ]
    return JsonResponse({'messages': messages_data})

@login_required
def clear_chat(request):
    if request.method == 'POST':
        ChatMessage.objects.all().delete()
        return redirect('index')  # Zorg dat 'index' correct gedefinieerd is in urls.py
    return HttpResponseBadRequest("Alleen POST toegelaten")
