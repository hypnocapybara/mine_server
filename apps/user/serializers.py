from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from apps.game.models import Game, GameStatusEnum


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')
    current_game = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_current_game(self, user):
        # bypass cross imports
        from apps.game.serializers import GameDetailSerializer
        game = Game.objects.filter(
            Q(Q(status=GameStatusEnum.IN_PROGRESS) | Q(status=GameStatusEnum.CREATED)) &
            Q(Q(first_player=user) | Q(second_player=user))).first()
        if not game:
            return None
        else:
            return GameDetailSerializer(game).data

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'password', 'token', 'current_game')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username')
