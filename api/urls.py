from . import views
from django.urls import path

urlpatterns = [
    path('messages/<str:pk>', views.get_messages_from_conversation),
    path('conversation/<str:pk>', views.get_conversation_from_message),
    path('user-conversation/<str:pk>', views.get_conversations_from_user),
    path('save-message/', views.create_new_message)
]