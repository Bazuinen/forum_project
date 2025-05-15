from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from devices.views import fingerprint_log_overzicht, fingerprint_log_detail, my_devices, collect_fingerprint


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
    path('clear-chat/', views.clear_chat, name='clear_chat'),

    path('collect_fingerprint/', collect_fingerprint, name='collect_fingerprint'),

    path("mijn-toestellen/", my_devices, name="my_devices"),
    path('mijn-toestellen/bezoek-logs/', fingerprint_log_overzicht, name='fingerprint_log_overzicht'),
    path('mijn-toestellen/bezoek-logs/<str:key>/', fingerprint_log_detail, name='fingerprint_log_detail'),
]
