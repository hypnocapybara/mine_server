from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.game.models import Game, GameStatusEnum


class StatsView(APIView):
    def get(self, request):
        # In real project it's better to store statistics in user model fields
        User = get_user_model()
        result = []
        for user in User.objects.all():
            result.append({
                'username': user.username,
                'wins': Game.objects.filter(
                    status=GameStatusEnum.WIN).filter(
                    Q(first_player=user) | Q(second_player=user)).count(),
                'losses': Game.objects.filter(
                    status=GameStatusEnum.LOSE).filter(
                    Q(first_player=user) | Q(second_player=user)).count(),
            })

        result.sort(key=lambda item: item['wins'], reverse=True)
        return Response(result)
