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
    path('current-user/', views.get_current_user)


]

# sorted_data = sorted(
#         serialized_convos.data,
#         key=lambda x:
#             max(datetime.datetime.strptime(msg['created_on'], '%d.%m.%Y %H:%M') for msg in x['messages']),
#         reverse=True)