from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('api.urls')),
                  path('dj-rest-auth/register/', include('dj_rest_auth.registration.urls')),
                  path('dj-rest-auth/signin/', LoginView.as_view()),
                  path('dj-rest-auth/logout/', LogoutView.as_view()),
                  path('dj-rest-auth/user/', UserDetailsView.as_view())
              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.LOCAL_SERVE_STATIC_FILES:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
# if settings.LOCAL_SERVE_MEDIA_FILES:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)