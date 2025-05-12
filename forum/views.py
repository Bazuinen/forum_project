from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Category, Topic, Post
from django.db.models import Count, Max
from django.shortcuts import get_object_or_404
from .forms import TopicForm
from .forms import PostForm
from django.http import JsonResponse
from .models import ChatMessage
from django.contrib.auth.decorators import login_required
from .models import FingerprintData
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from devices.models import LoginDevice


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    LoginDevice.objects.create(
        user=user,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        ip_address=ip
    )

def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def my_devices(request):
    devices = LoginDevice.objects.filter(user=request.user).order_by('-login_time')
    return render(request, 'devices/devices.html', {'devices': devices})

def index(request):
    categories = Category.objects.annotate(
        num_topics=Count('topic'),
        num_posts=Count('topic__posts'),
        latest_post_time=Max('topic__posts__created_at')
    )

    latest_posts = {}
    for category in categories:
        latest_post = (
            Post.objects
            .filter(topic__category=category)
            .order_by('-created_at')
            .select_related('created_by', 'topic')
            .first()
        )
        latest_posts[category.id] = latest_post

    # Voeg chat messages toe aan de context
    chat_messages = ChatMessage.objects.all().order_by('created_at')[:10]

    return render(request, 'forum/index.html', {
        'categories': categories,
        'latest_posts': latest_posts,
        'chat_messages': chat_messages  # <- BELANGRIJK
    })

# Voor het verzenden van een chatbericht via AJAX
@login_required
def send_chat_message(request):
    if request.method == "POST":
        message_content = request.POST.get('message')
        if message_content:
            chat_message = ChatMessage.objects.create(
                user=request.user,
                message=message_content
            )
            return JsonResponse({
                'status': 'success',
                'message': chat_message.message,
                'user': chat_message.user.username,
                'created_at': chat_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Bericht mag niet leeg zijn.'})
    return JsonResponse({'status': 'error', 'message': 'Ongeldige aanvraag.'})

# Voor het ophalen van de chatberichten via AJAX
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

@staff_member_required
def clear_chat(request):
    ChatMessage.objects.all().delete()
    return redirect('index')  # of waar je maar heen wilt

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Gebruiker aanmaken
            messages.success(request, "Je account is aangemaakt! Je kunt nu inloggen.")
            return redirect('login')  # Redirect naar de loginpagina
        else:
            messages.error(request, "Er is een fout opgetreden bij het aanmaken van je account.")
    else:
        form = UserCreationForm()

    return render(request, 'registration/registration.html', {'form': form})


def search(request):
    query = request.GET.get('q', '')
    results = None
    if query:
        results = Topic.objects.filter(title__icontains=query)
    return render(request, 'forum/search_results.html', {'results': results, 'query': query})

# Toon de onderwerpen van een specifieke categorie
def category_topics(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = Topic.objects.filter(category=category)  # Haal alle onderwerpen van deze categorie op
    return render(request, 'forum/category_topics.html', {'category': category, 'topics': topics})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = category.topic_set.all().order_by('-created_at')  # Nieuwste eerst
    return render(request, 'forum/category_detail.html', {'category': category, 'topics': topics})


@login_required
def create_topic(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        
        if form.is_valid():
            # Save the new topic, but don't commit to the database yet
            topic = form.save(commit=False)
            topic.category = category
            topic.created_by = request.user  # Associate the topic with the current user
            topic.save()

            # Create the first post for the topic
            post_content = request.POST.get('post_content')  # Get the content of the post

            if post_content:
                Post.objects.create(
                    topic=topic,
                    content=post_content,
                    created_by=request.user  # Associate the post with the current user
                )

                # Success message after both topic and post are created
                messages.success(request, "Het onderwerp is succesvol aangemaakt!")
                return redirect('topic_detail', topic_id=topic.id)  # Redirect to the topic detail page
            else:
                # If no post content is provided, display an error message
                messages.error(request, "Er moet inhoud worden ingevoerd voor het eerste bericht.")
                return render(request, 'forum/create_topic.html', {'form': form, 'category': category})

    else:
        form = TopicForm()

    return render(request, 'forum/create_topic.html', {'form': form, 'category': category})



def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Tel de views alleen op bij een GET-verzoek (dus geen refresh na POST)
    if request.method == 'GET':
        topic.views += 1
        topic.save()

    # Verwerk het formulier voor het toevoegen van een post
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.topic = topic
                post.created_by = request.user
                post.save()
                return redirect('topic_detail', topic_id=topic.id)
        else:
            return redirect('login')  # Verwijs naar login als niet ingelogd
    else:
        form = PostForm()

    posts = topic.posts.order_by('created_at')  # Chronologisch

    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'form': form,
        'posts': posts,
    })

@csrf_exempt
def collect_fingerprint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            FingerprintData.objects.create(
                ip_address = request.META.get('REMOTE_ADDR'),
                user_agent = data.get('user_agent', ''),
                screen_resolution = f"{data.get('screen_width')}x{data.get('screen_height')}",
                language = data.get('language', ''),
                timezone = data.get('timezone', ''),
                user = request.user if request.user.is_authenticated else None
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

@user_passes_test(lambda u: u.is_superuser)
def view_fingerprints(request):
    fingerprints = FingerprintData.objects.all().order_by('-timestamp')
    return render(request, 'devices\fingerprint_log.html', {'fingerprints': fingerprints})

