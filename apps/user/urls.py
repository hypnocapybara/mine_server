from django.urls import path

from apps.user.views import CustomAuthTokenView


urlpatterns = [
    path('login/', CustomAuthTokenView.as_view())
]
