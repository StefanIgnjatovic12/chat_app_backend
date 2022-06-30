from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('messages/<str:pk>', views.get_messages_from_conversation),
    path('conversation/<str:pk>', views.get_conversation_from_message),
    path('user-conversation/<str:pk>', views.get_conversations_from_user),
    path('user-conversation-brief/<str:pk>', views.get_partner_and_last_message_from_user),
    path('user-conversation-partner/<str:pk>/<str:name>', views.get_messages_with_user),
    path('save-message/', views.create_new_message),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-profile/<str:pk>', views.get_user_profile),
    path('reveal-profile/', views.reveal_profile),
    path('hide-profile/', views.hide_profile),
    path('revealed-profile-data/<str:pk>', views.get_revealed_profiles_from_convo),
    path('check-reveal-status/<str:pk>', views.check_reveal_status),
    path('edit-profile/', views.edit_profile),
    path('delete-convo/<str:pk>', views.delete_convo),
    path('profile-check-first-signin/', views.profile_check_on_first_signin),
    path('create-new-chat/', views.create_new_chat)
]
