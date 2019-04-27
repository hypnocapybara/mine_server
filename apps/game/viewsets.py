from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Game, GameStatusEnum
from .serializers import GameListSerializer, GameDetailSerializer, GameMarkSerializer
from .permissions import CanCreateGame, IsGamePlayer, CanStartGame, \
    CanJoinGame, CanTestField, CanFlagField


class GameViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = GameListSerializer
    queryset = Game.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':
            queryset = queryset.filter(status=GameStatusEnum.CREATED)

        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [CanCreateGame()]
        elif self.action == 'retrieve':
            return [IsGamePlayer()]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GameDetailSerializer
        else:
            return super().get_serializer_class()

    def create(self, request):
        return Response(GameDetailSerializer(
            Game.create_new_game(request.user)
        ).data)

    @action(methods=['PUT'], detail=True,
            permission_classes=[CanStartGame])
    def start(self, request, *args, **kwargs):
        game = self.get_object()
        game.start_single_game()
        return Response(GameDetailSerializer(game).data)

    @action(methods=['PUT'], detail=True,
            permission_classes=[CanJoinGame])
    def join(self, request, *args, **kwargs):
        game = self.get_object()
        game.join_game(request.user)
        return Response(GameDetailSerializer(game).data)

    @action(methods=['PUT'], detail=True,
            permission_classes=[CanTestField],
            serializer_class=GameMarkSerializer)
    def test(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        game.test_field([
            serializer.validated_data['x'],
            serializer.validated_data['y'],
        ])
        return Response(GameDetailSerializer(game).data)

    @action(methods=['PUT'], detail=True,
            permission_classes=[CanFlagField],
            serializer_class=GameMarkSerializer)
    def flag(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        game.flag_field([
            serializer.validated_data['x'],
            serializer.validated_data['y'],
        ])
        return Response(GameDetailSerializer(game).data)
