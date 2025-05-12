from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import view_fingerprints 
from devices.views import my_devices

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_topics, name='category_topics'),
    path('category/<int:category_id>/create_topic/', views.create_topic, name='create_topic'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'), 
    path('send-chat-message/', views.send_chat_message, name='send_chat_message'),
    path('get-chat-messages/', views.get_chat_messages, name='get_chat_messages'),
    path('systeem/bezoek-logs/', view_fingerprints, name='view_fingerprints'), 
    path('collect_fingerprint/', views.collect_fingerprint, name='collect_fingerprint'),
    path('clear-chat/', views.clear_chat, name='clear_chat'),
    path("mijn-toestellen/", my_devices, name="my_devices")


]
