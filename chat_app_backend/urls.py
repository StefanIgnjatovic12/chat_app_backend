"""chat_app_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserDetailsView
)
from dj_rest_auth.registration.views import RegisterView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('api.urls')),
                  path('dj-rest-auth/register/', include('dj_rest_auth.registration.urls')),
                  path('dj-rest-auth/signin/', LoginView.as_view()),
                  path('dj-rest-auth/logout/', LogoutView.as_view()),
                  path('dj-rest-auth/user/', UserDetailsView.as_view())

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
