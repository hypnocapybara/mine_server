from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from apps.game.models import Game, GameStatusEnum, GameTurnEnum


class CanCreateGame(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        player = request.user
        if Game.objects.filter(
            Q(Q(status=GameStatusEnum.CREATED) | Q(status=GameStatusEnum.IN_PROGRESS)) &
            Q(Q(first_player=player) | Q(second_player=player))
        ).exists():
            return False

        return True


class CanStartGame(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        return obj.first_player == request.user and obj.status == GameStatusEnum.CREATED


class CanJoinGame(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        if obj.second_player or obj.status != GameStatusEnum.CREATED:
            return False

        return True


class IsGamePlayer(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        player = request.user

        if player != obj.first_player and player != obj.second_player:
            return False

        return True


class CanTestField(IsGamePlayer):
    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        if obj.status != GameStatusEnum.IN_PROGRESS:
            return False

        if not obj.second_player:
            # Single player game
            return True

        player = request.user

        if (player == obj.first_player and obj.current_turn == GameTurnEnum.SECOND) or (
            player == obj.second_player and obj.current_turn == GameTurnEnum.FIRST):
            return False

        return True


class CanFlagField(CanTestField):
    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        return obj.rest_flags_count > 0
