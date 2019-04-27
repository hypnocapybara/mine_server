from rest_framework import serializers

from apps.user.serializers import UserListSerializer

from .models import Game


class GameListSerializer(serializers.ModelSerializer):
    first_player = UserListSerializer()
    second_player = UserListSerializer()

    class Meta:
        model = Game
        fields = ('pk', 'created', 'status', 'current_turn',
                  'first_player', 'second_player')


class GameDetailSerializer(GameListSerializer):
    field = serializers.SerializerMethodField()

    def get_field(self, game):
        result = []
        for i in range(game.field_size):
            result.append([])
            for g in range(game.field_size):
                result[i].append([])
                mark, visible, flagged = game.field[i][g]
                if visible:
                    result[i][g] = [mark, visible, flagged]
                else:
                    result[i][g] = [' ', False, flagged]
        return result

    class Meta(GameListSerializer.Meta):
        fields = GameListSerializer.Meta.fields + (
            'field', 'field_size', 'rest_flags_count')


class GameMarkSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
