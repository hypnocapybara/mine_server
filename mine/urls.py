from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from apps.user.viewsets import UserViewSet
from apps.game.viewsets import GameViewSet
from apps.game.views import StatsView


router = routers.DefaultRouter()
router.register('user', UserViewSet, base_name='user')
router.register('game', GameViewSet, base_name='game')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('stats/', StatsView.as_view()),

    path('user/', include('apps.user.urls')),
]
